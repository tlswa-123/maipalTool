"""
基础使用示例 - 快速开始
"""

from ai_voice_assistant import VoiceAssistant, create_simple_assistant


def example_basic():
    """示例1: 基础使用"""
    print("=" * 60)
    print("示例1: 基础使用")
    print("=" * 60)
    
    # 替换为你的 API key
    API_KEY = "your-api-key-here"
    
    # 创建助手
    assistant = create_simple_assistant(API_KEY)
    
    try:
        # 进行一次对话
        success, user_text, ai_response = assistant.chat_once()
        
        if success:
            print(f"\n✅ 对话完成")
            print(f"用户: {user_text}")
            print(f"AI: {ai_response}")
        else:
            print("\n❌ 对话失败")
    
    finally:
        assistant.cleanup()


def example_with_custom_config():
    """示例2: 自定义配置"""
    print("\n" + "=" * 60)
    print("示例2: 自定义配置")
    print("=" * 60)
    
    API_KEY = "your-api-key-here"
    
    # 创建自定义配置的助手
    assistant = VoiceAssistant(
        # STT 配置
        stt_engine='sphinx',  # 离线识别
        stt_language='zh-CN',
        
        # AI 配置
        ai_api_key=API_KEY,
        ai_model='gpt-3.5-turbo',
        ai_api_base='https://api.openai.com/v1',
        ai_system_prompt='你是一个专业的AI助手，请用简洁的语言回答。',
        
        # TTS 配置
        tts_engine='edge',
        tts_voice='zh-CN-YunxiNeural',  # 不同的声音
        
        # 其他
        auto_play_tts=True,
        show_text_during_playback=True
    )
    
    try:
        # 进行对话
        assistant.chat_loop(listen_method='once')
    
    finally:
        assistant.cleanup()


def example_streaming_mode():
    """示例3: 流式对话模式（边说边播）"""
    print("\n" + "=" * 60)
    print("示例3: 流式对话模式")
    print("=" * 60)
    
    API_KEY = "your-api-key-here"
    
    assistant = create_simple_assistant(API_KEY)
    
    try:
        # 使用流式对话模式
        assistant.chat_streaming(listen_method='once')
    
    finally:
        assistant.cleanup()


def example_with_callbacks():
    """示例4: 使用回调函数"""
    print("\n" + "=" * 60)
    print("示例4: 使用回调函数")
    print("=" * 60)
    
    API_KEY = "your-api-key-here"
    
    assistant = create_simple_assistant(API_KEY)
    
    # 设置回调函数
    def on_recognized(text):
        print(f"\n🔔 识别完成: {text}")
    
    def on_ai_response(response):
        print(f"\n🔔 AI 回复: {response}")
    
    def on_error(error):
        print(f"\n❌ 发生错误: {error}")
    
    assistant.set_on_recognized_callback(on_recognized)
    assistant.set_on_ai_response_callback(on_ai_response)
    assistant.set_on_error_callback(on_error)
    
    try:
        assistant.chat_loop(listen_method='once')
    
    finally:
        assistant.cleanup()


def example_with_ollama():
    """示例5: 使用本地 Ollama（无需 API key）"""
    print("\n" + "=" * 60)
    print("示例5: 使用本地 Ollama")
    print("=" * 60)
    
    # 使用 Ollama（需要先安装 Ollama）
    assistant = VoiceAssistant(
        stt_engine='sphinx',
        
        # Ollama 配置
        ai_api_key='ollama',  # Ollama 不需要 key
        ai_model='llama2',
        ai_api_base='http://localhost:11434/v1',
        
        tts_engine='edge',
        tts_voice='zh-CN-XiaoxiaoNeural'
    )
    
    try:
        print("\n✅ 使用本地 Ollama 模型")
        assistant.chat_loop(listen_method='once')
    
    finally:
        assistant.cleanup()


def example_change_settings():
    """示例6: 动态修改设置"""
    print("\n" + "=" * 60)
    print("示例6: 动态修改设置")
    print("=" * 60)
    
    API_KEY = "your-api-key-here"
    
    assistant = create_simple_assistant(API_KEY)
    
    try:
        # 修改 TTS 语音
        assistant.set_voice('zh-CN-YunxiNeural')
        
        # 修改语速
        assistant.set_rate(120)
        
        # 修改音量
        assistant.set_volume(80)
        
        # 修改系统提示词
        assistant.set_system_prompt('你是一个幽默的AI助手。')
        
        # 进行对话
        assistant.chat_loop(listen_method='once')
    
    finally:
        assistant.cleanup()


if __name__ == "__main__":
    # 运行示例
    # 取消注释你想运行的示例
    
    # example_basic()
    # example_with_custom_config()
    # example_streaming_mode()
    # example_with_callbacks()
    # example_with_ollama()
    example_change_settings()
