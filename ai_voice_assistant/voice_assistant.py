"""
语音助手主控制器
整合 STT、AI、TTS 三大模块，提供完整的语音对话功能
"""

import sys
import time
from typing import Optional, Callable
from pathlib import Path

from .stt_engine import STTEngine
from .ai_client import AIClient
from .tts_engine import TTSEngine


class VoiceAssistant:
    """AI 语音助手主控制器"""
    
    def __init__(self,
                 # STT 配置
                 stt_engine: str = 'sphinx',
                 stt_language: str = 'zh-CN',
                 
                 # AI 配置
                 ai_api_key: str = '',
                 ai_model: str = 'gpt-3.5-turbo',
                 ai_api_base: str = 'https://api.openai.com/v1',
                 ai_system_prompt: str = '你是一个友好、乐于助人的AI助手。',
                 
                 # TTS 配置
                 tts_engine: str = 'edge',
                 tts_voice: str = 'zh-CN-XiaoxiaoNeural',
                 
                 # 其他配置
                 auto_play_tts: bool = True,
                 show_text_during_playback: bool = True,
                 output_dir: str = './audio_output'):
        """
        初始化语音助手
        
        Args:
            stt_engine: 语音识别引擎
            stt_language: 识别语言
            ai_api_key: AI API 密钥
            ai_model: AI 模型名称
            ai_api_base: AI API 基础 URL
            ai_system_prompt: 系统提示词
            tts_engine: 语音合成引擎
            tts_voice: 合成语音
            auto_play_tts: 是否自动播放语音
            show_text_during_playback: 是否在播放时显示文字
            output_dir: 音频输出目录
        """
        self.auto_play_tts = auto_play_tts
        self.show_text_during_playback = show_text_during_playback
        self.is_running = False
        
        # 初始化 STT
        self.stt = STTEngine(
            engine=stt_engine,
            language=stt_language
        )
        
        # 初始化 AI
        self.ai = AIClient(
            api_key=ai_api_key,
            model=ai_model,
            api_base_url=ai_api_base,
            system_prompt=ai_system_prompt
        )
        
        # 初始化 TTS
        self.tts = TTSEngine(
            engine=tts_engine,
            voice=tts_voice,
            output_dir=output_dir
        )
        
        # 回调函数
        self.on_recognized: Optional[Callable] = None
        self.on_ai_response: Optional[Callable] = None
        self.on_error: Optional[Callable] = None
        
        print("=" * 60)
        print("🎙️  AI 语音助手已启动")
        print("=" * 60)
    
    def chat_once(self, listen_method: str = 'once') -> tuple[bool, str, str]:
        """
        进行一次对话
        
        Args:
            listen_method: 监听方式 ('once' 或 'silence')
        
        Returns:
            (success, user_text, ai_response)
        """
        try:
            # 1. 语音识别
            print("\n" + "=" * 60)
            
            if listen_method == 'silence':
                user_text = self.stt.listen_with_silence_detection(min_duration=1.0)
            else:
                user_text = self.stt.listen_once()
            
            if not user_text:
                return (False, "", "未能识别到语音")
            
            # 触发识别回调
            if self.on_recognized:
                self.on_recognized(user_text)
            
            print(f"\n💬 你: {user_text}")
            
            # 2. AI 对话
            ai_response = self.ai.chat(user_text)
            
            print(f"\n🤖 AI: {ai_response}")
            
            # 触发 AI 响应回调
            if self.on_ai_response:
                self.on_ai_response(ai_response)
            
            # 3. 语音合成
            if self.auto_play_tts and ai_response:
                print("\n🔊 正在播放语音...")
                self.tts.speak(ai_response, blocking=True)
            
            return (True, user_text, ai_response)
            
        except KeyboardInterrupt:
            print("\n⚠️  用户中断")
            return (False, "", "用户中断")
        except Exception as e:
            print(f"\n❌ 对话错误: {e}")
            if self.on_error:
                self.on_error(str(e))
            return (False, "", str(e))
    
    def chat_loop(self, listen_method: str = 'once'):
        """
        持续对话循环
        
        Args:
            listen_method: 监听方式 ('once' 或 'silence')
        """
        self.is_running = True
        print("\n🚀 进入对话模式")
        print("💡 提示: 按 Ctrl+C 退出\n")
        
        try:
            while self.is_running:
                success, user_text, ai_response = self.chat_once(listen_method)
                
                if not success:
                    # 如果用户主动中断或连续失败，退出
                    if "用户中断" in ai_response:
                        break
                    # 否则继续下一次对话
                    time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
        
        finally:
            self.stop()
    
    def chat_streaming(self, listen_method: str = 'once'):
        """
        流式对话模式（边说边播）
        
        Args:
            listen_method: 监听方式 ('once' 或 'silence')
        """
        self.is_running = True
        print("\n🚀 进入流式对话模式")
        print("💡 提示: 按 Ctrl+C 退出\n")
        
        # 设置流式输出回调
        accumulated_text = []
        
        def on_chunk(chunk: str):
            """处理 AI 返回的每一个字符"""
            accumulated_text.append(chunk)
            
            # 实时显示文字
            if self.show_text_during_playback:
                print(chunk, end='', flush=True)
        
        def on_complete(full_text: str):
            """AI 回复完成"""
            print()  # 换行
            
            # 播放完整语音
            if self.auto_play_tts and full_text:
                print("\n🔊 正在播放语音...")
                self.tts.speak(full_text, blocking=True)
        
        self.ai.set_on_message_callback(on_chunk)
        self.ai.set_on_complete_callback(on_complete)
        
        try:
            while self.is_running:
                # 语音识别
                print("\n" + "=" * 60)
                
                if listen_method == 'silence':
                    user_text = self.stt.listen_with_silence_detection(min_duration=1.0)
                else:
                    user_text = self.stt.listen_once()
                
                if not user_text:
                    continue
                
                print(f"\n💬 你: {user_text}")
                print(f"\n🤖 AI: ", end='', flush=True)
                
                # AI 对话（流式）
                accumulated_text = []
                self.ai.chat(user_text, stream=True)
                
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
        
        finally:
            self.stop()
    
    def stop(self):
        """停止对话"""
        self.is_running = False
        self.stt.stop_recording()
        print("\n🛑 对话已停止")
    
    def clear_history(self):
        """清空对话历史"""
        self.ai.clear_history()
    
    def set_system_prompt(self, prompt: str):
        """设置系统提示词"""
        self.ai.set_system_prompt(prompt)
    
    def set_voice(self, voice: str):
        """设置 TTS 语音"""
        self.tts.set_voice(voice)
    
    def set_rate(self, rate: int):
        """设置语速"""
        self.tts.set_rate(rate)
    
    def set_volume(self, volume: int):
        """设置音量"""
        self.tts.set_volume(volume)
    
    # 回调函数设置
    def set_on_recognized_callback(self, callback: Callable):
        """设置识别完成回调"""
        self.on_recognized = callback
    
    def set_on_ai_response_callback(self, callback: Callable):
        """设置 AI 响应回调"""
        self.on_ai_response = callback
    
    def set_on_error_callback(self, callback: Callable):
        """设置错误回调"""
        self.on_error = callback
    
    def cleanup(self):
        """清理所有资源"""
        print("\n🧹 正在清理资源...")
        self.stt.cleanup()
        self.tts.cleanup()
        print("✅ 清理完成")


# 快捷工厂函数
def create_simple_assistant(api_key: str) -> VoiceAssistant:
    """创建简单助手（使用默认配置）"""
    return VoiceAssistant(
        ai_api_key=api_key,
        stt_engine='sphinx',  # 离线识别
        tts_engine='edge'      # 在线合成
    )


def create_assistant_with_config(api_key: str,
                                 stt_engine: str = 'sphinx',
                                 stt_language: str = 'zh-CN',
                                 ai_model: str = 'gpt-3.5-turbo',
                                 ai_api_base: str = 'https://api.openai.com/v1',
                                 tts_engine: str = 'edge',
                                 tts_voice: str = 'zh-CN-XiaoxiaoNeural') -> VoiceAssistant:
    """创建自定义配置的助手"""
    return VoiceAssistant(
        ai_api_key=api_key,
        stt_engine=stt_engine,
        stt_language=stt_language,
        ai_model=ai_model,
        ai_api_base=ai_api_base,
        tts_engine=tts_engine,
        tts_voice=tts_voice
    )


# 简单的测试函数
def test_assistant():
    """测试语音助手"""
    print("=" * 60)
    print("🎙️  AI 语音助手测试")
    print("=" * 60)
    
    # 创建助手（替换为你的 API key）
    # api_key = "your-api-key-here"
    # 如果没有 API key，可以使用 Ollama（需要先安装）
    
    try:
        # 使用 Ollama（本地部署，无需 API key）
        from .ai_client import create_ollama_client
        
        # 创建助手
        assistant = VoiceAssistant(
            stt_engine='sphinx',  # 离线识别
            ai_api_key='ollama',  # Ollama 不需要 key
            ai_model='llama2',
            ai_api_base='http://localhost:11434/v1',
            tts_engine='edge',
            tts_voice='zh-CN-XiaoxiaoNeural'
        )
        
        print("\n✅ 使用本地 Ollama 模型")
        
    except:
        print("⚠️  请先配置 API key 或安装 Ollama")
        print("   OpenAI: api_key = 'your-openai-key'")
        print("   Ollama: 需要安装并启动 Ollama 服务")
        return
    
    try:
        # 启动对话
        assistant.chat_loop(listen_method='once')
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
    
    finally:
        assistant.cleanup()


if __name__ == "__main__":
    test_assistant()
