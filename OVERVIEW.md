# 🎙️ AI 语音助手 - 项目总览

一个功能完整、易于集成的 AI 语音对话助手 Python 模块。

## ✨ 核心特性

- 🎤 **智能语音识别** - 支持离线和在线识别，准确率高
- 🤖 **多 AI 服务支持** - OpenAI、智谱AI、DeepSeek、Ollama 等
- 🔊 **自然语音合成** - 逼真的语音播放，多种声音可选
- 🔌 **即插即用** - 模块化设计，几行代码即可集成
- ⚙️ **高度可配置** - 灵活的参数配置，满足不同需求
- 📱 **跨平台支持** - Windows、macOS、Linux 全平台支持

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API

复制 `.env.example` 为 `.env` 并填入你的 API key：

```bash
cp .env.example .env
# 编辑 .env 文件，填入 API_KEY=your-key
```

### 3. 运行

```bash
# 方式1: 使用快速启动脚本
python quick_start.py

# 方式2: 运行示例
python examples.py

# 方式3: 在代码中使用
python -c "from ai_voice_assistant import VoiceAssistant; ..."
```

## 📁 项目结构

```
ai_voice_assistant/
├── ai_voice_assistant/          # 核心模块
│   ├── __init__.py
│   ├── voice_assistant.py      # 主控制器
│   ├── stt_engine.py          # 语音识别
│   ├── ai_client.py           # AI 对话
│   ├── tts_engine.py          # 语音合成
│   └── config.py              # 配置管理
│
├── examples.py                 # 使用示例
├── quick_start.py             # 快速启动
├── requirements.txt           # 依赖清单
├── .env.example              # 配置示例
│
├── README.md                 # 使用说明
├── INTEGRATION.md           # 集成指南
└── PROJECT_STRUCTURE.md     # 结构说明
```

## 💻 使用示例

### 最简单的用法

```python
from ai_voice_assistant import create_simple_assistant

# 创建助手
assistant = create_simple_assistant(api_key="your-api-key")

# 开始对话
assistant.chat_loop()

# 清理资源
assistant.cleanup()
```

### 自定义配置

```python
from ai_voice_assistant import VoiceAssistant

assistant = VoiceAssistant(
    stt_engine='sphinx',           # 离线识别
    stt_language='zh-CN',
    ai_api_key='your-key',
    ai_model='gpt-3.5-turbo',
    tts_engine='edge',            # 在线合成
    tts_voice='zh-CN-XiaoxiaoNeural'
)

assistant.chat_loop()
```

### 只使用部分功能

```python
# 只用语音识别
from ai_voice_assistant.stt_engine import STTEngine
stt = STTEngine()
text = stt.listen_once()
print(f"识别结果: {text}")

# 只用 AI 对话
from ai_voice_assistant.ai_client import AIClient
ai = AIClient(api_key='your-key')
response = ai.chat('你好')
print(f"AI 回复: {response}")

# 只用语音合成
from ai_voice_assistant.tts_engine import TTSEngine
tts = TTSEngine()
tts.speak('你好，世界！')
```

## 🌟 支持的功能

### 语音识别 (STT)
- ✅ 离线识别 (Sphinx)
- ✅ 在线识别 (Whisper)
- ✅ 多语言支持
- ✅ 静音检测自动停止
- ✅ 音量可视化

### AI 对话
- ✅ 多 AI 服务支持
- ✅ 流式输出
- ✅ 对话历史管理
- ✅ 自定义系统提示词
- ✅ 本地部署支持 (Ollama)

### 语音合成 (TTS)
- ✅ 自然语音 (Edge TTS)
- ✅ 离线合成 (pyttsx3)
- ✅ 多种声音选择
- ✅ 语速/音量调节
- ✅ 保存为音频文件

### 高级功能
- ✅ 回调函数支持
- ✅ 流式对话（边说边播）
- ✅ 快捷指令
- ✅ 上下文管理
- ✅ 错误处理和重试

## 🔌 如何集成到你的 App

### 方式 1: 完整集成

复制整个 `ai_voice_assistant` 文件夹到你的项目：

```python
from ai_voice_assistant import VoiceAssistant

assistant = VoiceAssistant(ai_api_key='your-key')
assistant.chat_loop()
```

### 方式 2: 分模块集成

只使用你需要的功能：

```python
from ai_voice_assistant.stt_engine import STTEngine
from ai_voice_assistant.ai_client import AIClient
from ai_voice_assistant.tts_engine import TTSEngine

# 按需使用各个模块
```

### 方式 3: Web 应用集成

使用 WebSocket 实现实时对话：

```python
# 后端
from fastapi import FastAPI, WebSocket
from ai_voice_assistant import VoiceAssistant

app = FastAPI()
assistant = VoiceAssistant(ai_api_key='your-key')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # 实现 WebSocket 通信
```

### 方式 4: 移动应用集成

通过 Python 桥接调用：

```swift
// iOS
class VoiceAssistantManager {
    private var assistant: VoiceAssistant
    // 实现桥接调用
}
```

```kotlin
// Android
class VoiceAssistantManager {
    private val assistant: VoiceAssistant
    // 实现桥接调用
}
```

## 📖 文档

- **README.md** - 完整的使用说明和常见问题
- **INTEGRATION.md** - 详细的集成指南
- **PROJECT_STRUCTURE.md** - 项目结构说明
- **examples.py** - 丰富的使用示例

## 🔧 配置说明

### AI 服务

| 服务 | 说明 | 免费额度 |
|------|------|----------|
| OpenAI | 最流行 | 需付费 |
| 智谱AI | 国内优秀 | 有免费额度 |
| DeepSeek | 高性价比 | 有免费额度 |
| Ollama | 本地部署 | 完全免费 |

### 语音识别

| 引擎 | 类型 | 优点 |
|------|------|------|
| Sphinx | 离线 | 免费、无需网络 |
| Whisper | 在线 | 准确率高 |

### 语音合成

| 引擎 | 类型 | 优点 |
|------|------|------|
| Edge TTS | 在线 | 语音自然、流畅 |
| pyttsx3 | 离线 | 无需网络 |

## 🎯 适用场景

- 📱 手机 App 语音助手
- 💬 智能客服系统
- 🎓 教育辅导应用
- 🏠 智能家居控制
- 🚗 车载语音助手
- 💼 办公助手
- 🎮 游戏语音交互
- 🏥 医疗语音助手

## ⚡ 性能

- **语音识别**: 1-3 秒（取决于引擎）
- **AI 对话**: 1-5 秒（取决于模型）
- **语音合成**: 即时播放
- **内存占用**: ~100MB

## 🛠️ 技术栈

- **语言**: Python 3.8+
- **语音识别**: SpeechRecognition, Whisper
- **AI 对话**: OpenAI API, Ollama
- **语音合成**: edge-tts, pyttsx3
- **音频处理**: PyAudio, NumPy

## 📝 开发路线图

- [ ] 支持更多 AI 服务
- [ ] 语音克隆功能
- [ ] 多轮对话优化
- [ ] 情感识别
- [ ] 语音指令识别
- [ ] 多语言界面
- [ ] GUI 界面

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🆘 获取帮助

- 查看 README.md 中的常见问题
- 查看 INTEGRATION.md 中的集成指南
- 运行 examples.py 查看示例代码

---

**祝你使用愉快！** 🎉

如有问题，欢迎反馈！
