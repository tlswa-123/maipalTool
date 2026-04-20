"""
语音合成引擎 (Text-to-Speech)
支持多种合成引擎，可灵活切换
"""

import os
import threading
import time
from typing import Optional
from pathlib import Path


class TTSEngine:
    """语音合成引擎"""
    
    def __init__(self,
                 engine: str = 'edge',
                 voice: str = 'zh-CN-XiaoxiaoNeural',
                 rate: int = 100,
                 volume: int = 100,
                 output_dir: str = './audio_output'):
        """
        初始化语音合成引擎
        
        Args:
            engine: 合成引擎 ('edge' 或 'pyttsx3')
            voice: 语音名称
            rate: 语速百分比 (50-200)
            volume: 音量百分比 (0-100)
            output_dir: 音频文件输出目录
        """
        self.engine = engine
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.output_dir = output_dir
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 初始化引擎
        self._init_engine()
        
        print(f"✅ TTS 引擎初始化完成")
        print(f"   引擎: {engine}")
        print(f"   语音: {voice}")
    
    def _init_engine(self):
        """初始化具体的 TTS 引擎"""
        if self.engine == 'edge':
            self._init_edge_tts()
        elif self.engine == 'pyttsx3':
            self._init_pyttsx3()
        else:
            raise ValueError(f"不支持的引擎: {self.engine}")
    
    def _init_edge_tts(self):
        """初始化 Edge TTS"""
        try:
            import edge_tts
            self.edge_tts = edge_tts
            self.pyttsx3_engine = None
        except ImportError:
            print("⚠️  edge-tts 未安装，正在回退到 pyttsx3")
            print("   安装命令: pip install edge-tts")
            self.engine = 'pyttsx3'
            self._init_pyttsx3()
    
    def _init_pyttsx3(self):
        """初始化 pyttsx3"""
        try:
            import pyttsx3
            self.pyttsx3_engine = pyttsx3.init()
            self.edge_tts = None
            
            # 设置参数
            voices = self.pyttsx3_engine.getProperty('voices')
            if voices:
                # 尝试选择中文语音
                for v in voices:
                    if 'zh' in v.languages[0].lower() or 'chinese' in v.name.lower():
                        self.pyttsx3_engine.setProperty('voice', v.id)
                        break
            
            self.pyttsx3_engine.setProperty('rate', self.rate)
            self.pyttsx3_engine.setProperty('volume', self.volume / 100.0)
            
        except ImportError:
            print("❌ pyttsx3 未安装")
            print("   安装命令: pip install pyttsx3")
            raise
    
    def speak(self, text: str, blocking: bool = True) -> bool:
        """
        朗读文字
        
        Args:
            text: 要朗读的文字
            blocking: 是否阻塞等待播放完成
        
        Returns:
            是否成功
        """
        if not text or not text.strip():
            return False
        
        try:
            if self.engine == 'edge':
                return self._speak_edge(text, blocking)
            else:  # pyttsx3
                return self._speak_pyttsx3(text, blocking)
        except Exception as e:
            print(f"❌ 语音合成错误: {e}")
            return False
    
    def _speak_edge(self, text: str, blocking: bool) -> bool:
        """使用 Edge TTS 朗读"""
        if not self.edge_tts:
            return False
        
        try:
            # 生成音频文件
            communicate = self.edge_tts.Communicate(text, self.voice)
            
            # 保存到临时文件
            timestamp = int(time.time())
            temp_file = os.path.join(self.output_dir, f"temp_{timestamp}.mp3")
            
            await_flag = communicate.save(temp_file)
            
            if blocking:
                # 播放音频
                return self._play_audio(temp_file, blocking=True)
            else:
                # 异步播放
                thread = threading.Thread(
                    target=self._play_audio,
                    args=(temp_file, True)
                )
                thread.daemon = True
                thread.start()
                return True
                
        except Exception as e:
            print(f"Edge TTS 错误: {e}")
            return False
    
    def _speak_pyttsx3(self, text: str, blocking: bool) -> bool:
        """使用 pyttsx3 朗读"""
        if not self.pyttsx3_engine:
            return False
        
        try:
            if blocking:
                self.pyttsx3_engine.say(text)
                self.pyttsx3_engine.runAndWait()
                return True
            else:
                # pyttsx3 不支持异步，需要单独的引擎实例
                def speak_async():
                    engine = self.pyttsx3_engine.__class__.init()
                    engine.say(text)
                    engine.runAndWait()
                
                thread = threading.Thread(target=speak_async)
                thread.daemon = True
                thread.start()
                return True
                
        except Exception as e:
            print(f"pyttsx3 错误: {e}")
            return False
    
    def _play_audio(self, audio_file: str, blocking: bool) -> bool:
        """播放音频文件"""
        try:
            # macOS
            if os.name == 'posix':
                import subprocess
                if blocking:
                    subprocess.run(['afplay', audio_file], check=True)
                else:
                    subprocess.Popen(['afplay', audio_file])
            # Windows
            elif os.name == 'nt':
                import winsound
                if blocking:
                    winsound.PlaySound(audio_file, winsound.SND_FILENAME)
                else:
                    import threading
                    thread = threading.Thread(
                        target=winsound.PlaySound,
                        args=(audio_file, winsound.SND_FILENAME)
                    )
                    thread.start()
            # Linux
            else:
                import subprocess
                if blocking:
                    subprocess.run(['aplay', audio_file], check=True)
                else:
                    subprocess.Popen(['aplay', audio_file])
            
            # 删除临时文件
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            return True
        except Exception as e:
            print(f"播放音频错误: {e}")
            return False
    
    def save_to_file(self, text: str, output_path: str) -> bool:
        """
        将语音保存到文件
        
        Args:
            text: 要合成的文字
            output_path: 输出文件路径
        
        Returns:
            是否成功
        """
        if not text or not text.strip():
            return False
        
        try:
            if self.engine == 'edge' and self.edge_tts:
                communicate = self.edge_tts.Communicate(text, self.voice)
                communicate.save(output_path)
                print(f"✅ 音频已保存到: {output_path}")
                return True
            else:
                print("❌ 只有 Edge TTS 支持保存到文件")
                return False
                
        except Exception as e:
            print(f"保存音频错误: {e}")
            return False
    
    def set_voice(self, voice: str):
        """设置语音"""
        self.voice = voice
        print(f"✅ 语音已更改为: {voice}")
    
    def set_rate(self, rate: int):
        """设置语速"""
        self.rate = max(50, min(200, rate))
        if self.pyttsx3_engine:
            self.pyttsx3_engine.setProperty('rate', self.rate)
        print(f"✅ 语速已设置为: {self.rate}%")
    
    def set_volume(self, volume: int):
        """设置音量"""
        self.volume = max(0, min(100, volume))
        if self.pyttsx3_engine:
            self.pyttsx3_engine.setProperty('volume', self.volume / 100.0)
        print(f"✅ 音量已设置为: {self.volume}%")
    
    def list_voices(self):
        """列出可用语音（仅 edge-tts）"""
        if self.engine != 'edge' or not self.edge_tts:
            print("❌ 只有 Edge TTS 支持列出语音")
            return []
        
        try:
            import asyncio
            voices = []
            
            async def get_voices():
                nonlocal voices
                voices = await self.edge_tts.list_voices()
            
            asyncio.run(get_voices())
            
            # 按语言分类显示
            voice_dict = {}
            for v in voices:
                locale = v['Locale']
                if locale not in voice_dict:
                    voice_dict[locale] = []
                voice_dict[locale].append(v['Name'])
            
            print("\n📋 可用语音:")
            for locale, names in sorted(voice_dict.items()):
                print(f"\n{locale}:")
                for name in names[:5]:  # 只显示前5个
                    print(f"  - {name}")
                if len(names) > 5:
                    print(f"  ... 还有 {len(names)-5} 个语音")
            
            return voices
            
        except Exception as e:
            print(f"获取语音列表错误: {e}")
            return []
    
    def cleanup(self):
        """清理资源"""
        if self.pyttsx3_engine:
            try:
                self.pyttsx3_engine.stop()
            except:
                pass
        print("🧹 TTS 资源已清理")


# 简单的测试函数
def test_tts():
    """测试语音合成"""
    print("=" * 50)
    print("🔊 语音合成测试")
    print("=" * 50)
    
    # 创建引擎（使用 edge-tts，推荐）
    tts = TTSEngine(
        engine='edge',
        voice='zh-CN-XiaoxiaoNeural',
        rate=100,
        volume=80
    )
    
    # 或者使用 pyttsx3（离线）
    # tts = TTSEngine(
    #     engine='pyttsx3',
    #     rate=150,
    #     volume=80
    # )
    
    try:
        # 列出可用语音（仅 edge-tts）
        # tts.list_voices()
        
        # 测试朗读
        text = "你好！我是AI语音助手。很高兴为你服务。"
        
        print(f"\n要朗读的文字: {text}")
        print("正在播放...\n")
        
        tts.speak(text, blocking=True)
        
        print("\n✅ 播放完成")
        
        # 保存到文件
        # output_file = './audio_output/test.mp3'
        # tts.save_to_file(text, output_file)
        
    except KeyboardInterrupt:
        print("\n⚠️  用户中断")
    
    finally:
        tts.cleanup()


if __name__ == "__main__":
    test_tts()
