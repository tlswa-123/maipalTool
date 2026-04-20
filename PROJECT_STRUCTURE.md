# 项目结构说明

```
ai_voice_assistant/
├── ai_voice_assistant/          # 📦 核心模块（可独立使用）
│   ├── __init__.py             # 模块入口，导出主要类
│   ├── voice_assistant.py      # 主控制器，整合所有功能
│   ├── stt_engine.py          # 语音识别引擎 (STT)
│   ├── ai_client.py           # AI 对话客户端
│   ├── tts_engine.py          # 语音合成引擎 (TTS)
│   └── config.py              # 配置管理
│
├── examples.py                 # 📚 使用示例
├── quick_start.py             # 🚀 快速启动脚本
├── requirements.txt           # 📋 依赖清单
├── .env.example              # ⚙️  环境变量示例
├── .gitignore               # 🚫 Git 忽略文件
│
├── README.md                # 📖 项目说明文档
├── INTEGRATION.md           # 📦 集成指南
└── PROJECT_STRUCTURE.md     # 📂 本文件 - 项目结构说明
```

## 📦 核心模块说明

### `ai_voice_assistant/` - 核心模块

这是整个语音助手的核心，可以独立复制到任何项目中使用。

#### `__init__.py`
- 模块入口文件
- 导出主要类：`VoiceAssistant`, `STTEngine`, `AIClient`, `TTSEngine`
- 提供版本信息

#### `voice_assistant.py`
- **主控制器类**
- 整合 STT、AI、TTS 三大模块
- 提供完整的语音对话功能
- 主要类：`VoiceAssistant`

主要功能：
- `chat_once()` - 进行一次对话
- `chat_loop()` - 持续对话循环
- `chat_streaming()` - 流式对话（边说边播）
- 回调函数支持
- 配置管理

#### `stt_engine.py`
- **语音识别引擎**
- 支持多种识别引擎
- 主要类：`STTEngine`

支持的引擎：
- `sphinx` - 离线识别（默认）
- `whisper` - 在线识别（更准确）

主要功能：
- `listen_once()` - 监听一次（按 Enter 停止）
- `listen_with_silence_detection()` - 静音检测自动停止
- 噪音校准
- 音量可视化

#### `ai_client.py`
- **AI 对话客户端**
- 支持多种 AI 服务
- 主要类：`AIClient`

支持的服务：
- OpenAI (默认)
- 智谱 AI
- DeepSeek
- Ollama (本地)

主要功能：
- `chat()` - 发送消息
- 流式输出支持
- 对话历史管理
- 系统提示词设置

#### `tts_engine.py`
- **语音合成引擎**
- 支持多种合成引擎
- 主要类：`TTSEngine`

支持的引擎：
- `edge-tts` - Edge TTS（推荐，语音自然）
- `pyttsx3` - 离线合成

主要功能：
- `speak()` - 朗读文字
- `save_to_file()` - 保存到音频文件
- 语音列表查看
- 语速、音量调节

#### `config.py`
- **配置管理**
- 统一管理所有配置参数
- 提供预设配置
- 主要类：`Config`

配置类别：
- STT 配置（识别引擎、语言、录音参数）
- AI 配置（API、模型、对话参数）
- TTS 配置（合成引擎、语音、播放参数）
- 系统配置（提示词、调试选项）

## 📚 辅助文件说明

### `examples.py` - 使用示例
包含多个详细示例，展示各种使用方式：
- 基础使用
- 自定义配置
- 流式对话模式
- 使用回调函数
- 使用本地 Ollama
- 动态修改设置

运行方式：
```bash
python examples.py
```

### `quick_start.py` - 快速启动
一键启动脚本，简化使用流程：
- 自动检查依赖
- 交互式配置
- 友好的用户界面
- 错误处理

运行方式：
```bash
python quick_start.py
```

### `requirements.txt` - 依赖清单
项目所需的所有 Python 包：
- `SpeechRecognition` - 语音识别
- `pyaudio` - 音频处理
- `requests` - HTTP 请求
- `edge-tts` - 语音合成
- `pyttsx3` - 离线语音合成
- `numpy` - 数值计算

安装方式：
```bash
pip install -r requirements.txt
```

### `.env.example` - 环境变量示例
环境变量配置模板，复制为 `.env` 后填入实际配置。

配置项包括：
- AI API 配置
- STT 配置
- TTS 配置
- 系统配置

### `.gitignore` - Git 忽略文件
指定不需要纳入版本控制的文件：
- Python 缓存文件
- 虚拟环境
- 环境变量 (.env)
- 音频输出文件
- 日志文件

## 📖 文档说明

### `README.md` - 项目说明
主要文档，包含：
- 功能特性介绍
- 安装指南
- 快速开始
- 详细文档
- 常见问题

### `INTEGRATION.md` - 集成指南
详细的集成指南，包含：
- 多种集成方式
- 不同平台示例
- 高级集成技巧
- 完整示例项目结构
- 集成检查清单

### `PROJECT_STRUCTURE.md` - 项目结构说明
本文件，说明：
- 项目目录结构
- 各文件功能
- 模块关系

## 🎯 如何使用

### 方式 1: 快速启动

```bash
python quick_start.py
```

### 方式 2: 运行示例

```bash
python examples.py
```

### 方式 3: 在代码中使用

```python
from ai_voice_assistant import VoiceAssistant

assistant = VoiceAssistant(
    ai_api_key='your-api-key',
    stt_engine='sphinx',
    tts_engine='edge'
)

assistant.chat_loop()
```

### 方式 4: 只使用部分功能

```python
# 只用语音识别
from ai_voice_assistant.stt_engine import STTEngine
stt = STTEngine()
text = stt.listen_once()

# 只用 AI 对话
from ai_voice_assistant.ai_client import AIClient
ai = AIClient(api_key='your-key')
response = ai.chat('你好')

# 只用语音合成
from ai_voice_assistant.tts_engine import TTSEngine
tts = TTSEngine()
tts.speak('你好')
```

## 🔄 模块关系图

```
VoiceAssistant (主控制器)
    ├── STTEngine (语音识别)
    │   └── SpeechRecognition / Whisper
    ├── AIClient (AI 对话)
    │   └── OpenAI / 智谱AI / DeepSeek / Ollama
    └── TTSEngine (语音合成)
        └── edge-tts / pyttsx3
```

## 💡 扩展建议

如果需要扩展功能，可以在 `ai_voice_assistant/` 目录下添加新模块：

- `audio_player.py` - 高级音频播放器
- `conversation_history.py` - 对话历史管理
- `persona_manager.py` - AI 人设管理
- `shortcut_handler.py` - 快捷指令处理
- `emotion_analyzer.py` - 情感分析
- `voice_cloning.py` - 语音克隆

## 📝 开发规范

1. **命名规范**
   - 类名：大驼峰 (PascalCase)
   - 函数/变量：小写加下划线 (snake_case)
   - 常量：全大写加下划线 (UPPER_SNAKE_CASE)

2. **文档规范**
   - 每个模块都有文档字符串
   - 每个函数都有参数说明
   - 重要代码有注释

3. **错误处理**
   - 关键操作有 try-except
   - 提供友好的错误提示
   - 资源正确清理

4. **测试**
   - 每个模块都有 `__main__` 测试代码
   - 可以独立运行测试

---

祝你使用愉快！🎉
