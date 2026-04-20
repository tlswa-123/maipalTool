"""
AI语音对话助手 - 独立可插拔组件

这个模块提供了一个完整的语音对话系统，可以轻松集成到任何应用中。
"""

# 尝试导入各个模块，如果依赖缺失则跳过
try:
    from .voice_assistant import VoiceAssistant
    _has_voice_assistant = True
except ImportError as e:
    _has_voice_assistant = False
    VoiceAssistant = None

try:
    from .stt_engine import STTEngine
    _has_stt = True
except ImportError as e:
    _has_stt = False
    STTEngine = None

try:
    from .ai_client import AIClient
    _has_ai = True
except ImportError as e:
    _has_ai = False
    AIClient = None

try:
    from .tts_engine import TTSEngine
    _has_tts = True
except ImportError as e:
    _has_tts = False
    TTSEngine = None

__version__ = "1.0.0"

# 根据可用性导出
__all__ = []

if VoiceAssistant:
    __all__.append('VoiceAssistant')
if STTEngine:
    __all__.append('STTEngine')
if AIClient:
    __all__.append('AIClient')
if TTSEngine:
    __all__.append('TTSEngine')
