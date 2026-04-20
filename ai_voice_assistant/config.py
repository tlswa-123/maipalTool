"""
配置文件 - 管理所有语音助手的配置参数
"""

import os
from typing import Optional


class Config:
    """语音助手配置类"""
    
    # ==================== 语音识别(STT)配置 ====================
    # 使用的识别引擎: 'sphinx' (离线, 默认) 或 'whisper' (在线, 更准确)
    STT_ENGINE = os.getenv('STT_ENGINE', 'sphinx')
    
    # 识别语言
    STT_LANGUAGE = os.getenv('STT_LANGUAGE', 'zh-CN')  # 中文
    # STT_LANGUAGE = os.getenv('STT_LANGUAGE', 'en-US')  # 英文
    
    # Whisper 模型大小 (仅在使用 whisper 时有效)
    # tiny/base/small/medium/large
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')
    
    # 录音参数
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1024'))      # 音频块大小
    SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', '16000'))  # 采样率
    CHANNELS = int(os.getenv('CHANNELS', '1'))             # 声道数
    
    # 静音检测阈值 (用于自动停止录音)
    SILENCE_THRESHOLD = int(os.getenv('SILENCE_THRESHOLD', '500'))
    SILENCE_DURATION = float(os.getenv('SILENCE_DURATION', '1.0'))  # 静音持续多少秒停止
    
    # ==================== AI 对话配置 ====================
    # AI 服务提供商: 'openai', 'zhipu', 'qwen', 'deepseek', 'ollama' 等
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')
    
    # API 密钥
    API_KEY = os.getenv('API_KEY', '')
    
    # API 基础 URL (可选，用于私有化部署)
    API_BASE_URL = os.getenv('API_BASE_URL', '')
    
    # 模型名称
    MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
    
    # 对话参数
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '500'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # ==================== 语音合成(TTS)配置 ====================
    # 使用的合成引擎: 'edge' (推荐), 'pyttsx3' (离线)
    TTS_ENGINE = os.getenv('TTS_ENGINE', 'edge')
    
    # Edge TTS 语音 (中文示例: zh-CN-XiaoxiaoNeural, zh-CN-YunxiNeural)
    EDGE_VOICE = os.getenv('EDGE_VOICE', 'zh-CN-XiaoxiaoNeural')
    # EDGE_VOICE = os.getenv('EDGE_VOICE', 'en-US-JennyNeural')  # 英文示例
    
    # 语速和音调
    TTS_RATE = int(os.getenv('TTS_RATE', '100'))      # 语速百分比
    TTS_VOLUME = int(os.getenv('TTS_VOLUME', '100'))  # 音量百分比
    
    # ==================== 系统提示词 ====================
    SYSTEM_PROMPT = os.getenv(
        'SYSTEM_PROMPT',
        "你是一个友好、乐于助人的AI助手。请用简洁、自然的语言回答用户的问题。"
    )
    
    # ==================== 其他配置 ====================
    # 是否显示详细日志
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # 是否在播放语音的同时显示文字
    SHOW_TEXT_DURING_PLAYBACK = True
    
    # 会话历史最大条数
    MAX_HISTORY = int(os.getenv('MAX_HISTORY', '10'))
    
    @classmethod
    def validate(cls) -> bool:
        """验证配置是否完整"""
        if not cls.API_KEY:
            print("⚠️  警告: API_KEY 未设置，AI 功能将无法使用")
            print(f"   请设置环境变量或直接修改: API_KEY = 'your-api-key'")
            return False
        return True


# 创建默认配置实例
default_config = Config()


# 快捷方法：获取预设配置
def get_preset_config(provider: str = 'openai') -> Config:
    """
    获取预设配置
    
    Args:
        provider: AI 提供商 ('openai', 'zhipu', 'deepseek', 'ollama')
    
    Returns:
        Config: 配置实例
    """
    config = Config()
    
    presets = {
        'openai': {
            'AI_PROVIDER': 'openai',
            'API_BASE_URL': 'https://api.openai.com/v1',
            'MODEL_NAME': 'gpt-3.5-turbo',
        },
        'zhipu': {
            'AI_PROVIDER': 'zhipu',
            'API_BASE_URL': 'https://open.bigmodel.cn/api/paas/v4',
            'MODEL_NAME': 'glm-4',
        },
        'deepseek': {
            'AI_PROVIDER': 'openai',  # DeepSeek 兼容 OpenAI API
            'API_BASE_URL': 'https://api.deepseek.com/v1',
            'MODEL_NAME': 'deepseek-chat',
        },
        'ollama': {
            'AI_PROVIDER': 'ollama',
            'API_BASE_URL': 'http://localhost:11434/v1',
            'MODEL_NAME': 'llama2',
        },
    }
    
    if provider in presets:
        for key, value in presets[provider].items():
            setattr(config, key, value)
    
    return config
