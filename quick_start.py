#!/usr/bin/env python3
"""
快速启动脚本 - 一键运行 AI 语音助手
"""

import sys
import os
from pathlib import Path

# 添加项目路径到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai_voice_assistant import VoiceAssistant, create_simple_assistant
from ai_voice_assistant.config import get_preset_config


def print_banner():
    """打印欢迎横幅"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           🎙️  AI 语音助手 - 快速启动 🎙️                 ║
║                                                          ║
║          一个功能完整的语音对话系统                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def check_dependencies():
    """检查依赖是否安装"""
    print("\n📦 检查依赖...")
    
    required_packages = {
        'SpeechRecognition': 'speech_recognition',
        'pyaudio': 'pyaudio',
        'requests': 'requests',
        'edge_tts': 'edge_tts',
        'pyttsx3': 'pyttsx3',
        'numpy': 'numpy'
    }
    
    missing = []
    
    for name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} (未安装)")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  缺少 {len(missing)} 个依赖包")
        print("💡 请运行: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ 所有依赖已安装")
        return True


def get_api_key():
    """获取 API key"""
    # 1. 从环境变量读取
    api_key = os.getenv('API_KEY', '')
    
    if api_key:
        return api_key
    
    # 2. 从 .env 文件读取
    env_file = project_root / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    if api_key:
                        return api_key
    
    # 3. 提示用户输入
    print("\n" + "=" * 60)
    print("🔑 请选择 AI 服务:")
    print("=" * 60)
    print("1. OpenAI (需要 API key)")
    print("2. 智谱 AI (需要 API key)")
    print("3. DeepSeek (需要 API key)")
    print("4. Ollama (本地部署，无需 API key)")
    print("5. 退出")
    
    choice = input("\n请选择 (1-5): ").strip()
    
    if choice == '1':
        api_key = input("请输入 OpenAI API key: ").strip()
        if not api_key:
            print("❌ API key 不能为空")
            return None
        return api_key
    elif choice == '2':
        api_key = input("请输入智谱 AI API key: ").strip()
        if not api_key:
            print("❌ API key 不能为空")
            return None
        return api_key
    elif choice == '3':
        api_key = input("请输入 DeepSeek API key: ").strip()
        if not api_key:
            print("❌ API key 不能为空")
            return None
        return api_key
    elif choice == '4':
        return 'ollama'
    elif choice == '5':
        return None
    else:
        print("❌ 无效选择")
        return None


def create_assistant(api_key):
    """创建助手实例"""
    if api_key == 'ollama':
        print("\n🔄 使用本地 Ollama 模型...")
        config = get_preset_config('ollama')
        
        assistant = VoiceAssistant(
            stt_engine='sphinx',
            stt_language='zh-CN',
            ai_api_key='ollama',
            ai_model='llama2',
            ai_api_base='http://localhost:11434/v1',
            ai_system_prompt='你是一个友好、乐于助人的AI助手。',
            tts_engine='edge',
            tts_voice='zh-CN-XiaoxiaoNeural',
            auto_play_tts=True
        )
        
    elif 'bigmodel' in str(api_key).lower():
        print("\n🔄 使用智谱 AI 模型...")
        config = get_preset_config('zhipu')
        
        assistant = VoiceAssistant(
            stt_engine='sphinx',
            stt_language='zh-CN',
            ai_api_key=api_key,
            ai_model='glm-4',
            ai_api_base='https://open.bigmodel.cn/api/paas/v4',
            ai_system_prompt='你是一个友好、乐于助人的AI助手。',
            tts_engine='edge',
            tts_voice='zh-CN-XiaoxiaoNeural',
            auto_play_tts=True
        )
        
    else:
        # 默认使用 OpenAI 兼容格式
        print("\n🔄 使用 AI 模型...")
        config = get_preset_config('openai')
        
        assistant = VoiceAssistant(
            stt_engine='sphinx',
            stt_language='zh-CN',
            ai_api_key=api_key,
            ai_model='gpt-3.5-turbo',
            ai_api_base='https://api.openai.com/v1',
            ai_system_prompt='你是一个友好、乐于助人的AI助手。',
            tts_engine='edge',
            tts_voice='zh-CN-XiaoxiaoNeural',
            auto_play_tts=True
        )
    
    return assistant


def main():
    """主函数"""
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请先安装依赖")
        return
    
    # 获取 API key
    api_key = get_api_key()
    if not api_key:
        print("\n👋 再见！")
        return
    
    # 创建助手
    try:
        assistant = create_assistant(api_key)
    except Exception as e:
        print(f"\n❌ 创建助手失败: {e}")
        return
    
    # 启动对话
    print("\n" + "=" * 60)
    print("🚀 AI 语音助手已启动")
    print("=" * 60)
    print("\n💡 使用说明:")
    print("   - 对着麦克风说话")
    print("   - AI 会识别并回复")
    print("   - 按 Ctrl+C 退出")
    print("\n💡 提示:")
    print("   - 首次使用可能需要几秒钟初始化")
    print("   - 确保麦克风已连接")
    print("   - 在安静的环境中使用效果更好")
    
    try:
        # 进入对话循环
        assistant.chat_loop(listen_method='once')
        
    except KeyboardInterrupt:
        print("\n\n👋 感谢使用 AI 语音助手，再见！")
    
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
    
    finally:
        # 清理资源
        print("\n🧹 正在清理资源...")
        assistant.cleanup()
        print("✅ 清理完成")


if __name__ == "__main__":
    main()
