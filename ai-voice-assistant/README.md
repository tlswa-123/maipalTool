# AI 语音助手 🎙️

一个功能完整、易于集成的 AI 语音对话助手 Python 模块。

## ✨ 特性

- 🎤 **语音识别 (STT)** - 支持离线 (Sphinx) 和在线 (Whisper) 识别
- 🤖 **AI 对话** - 支持多种 AI 服务 (OpenAI, 智谱AI, DeepSeek, Ollama 等)
- 🔊 **语音合成 (TTS)** - 支持自然流畅的语音播放 (Edge TTS)
- 🔌 **易于集成** - 模块化设计，可轻松嵌入任何应用
- ⚙️ **高度可配置** - 灵活的参数配置，满足不同需求
- 🚀 **即插即用** - 提供简单 API，几行代码即可使用

## 📦 安装

### 1. 克隆或下载此项目

```bash
cd ai_voice_assistant
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. (可选) 安装 PortAudio (macOS/Linux)

**macOS:**
```bash
brew install portaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev
```

**Windows:**
通常已包含，无需额外安装。

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API key：

```env
API_KEY=your-api-key-here
```

## 🚀 快速开始

### 基础用法

```python
from ai_voice_assistant import create_simple_assistant

# 创建助手（替换为你的 API key）
assistant = create_simple_assistant(api_key="your-api-key-here")

try:
    # 进行对话
    assistant.chat_loop()
finally:
    assistant.cleanup()
```

### 自定义配置

```python
from ai_voice_assistant import VoiceAssistant

assistant = VoiceAssistant(
    # STT 配置
    stt_engine='sphinx',  # 离线识别
    stt_language='zh-CN',
    
    # AI 配置
    ai_api_key='your-api-key-here',
    ai_model='gpt-3.5-turbo',
    ai_api_base='https://api.openai.com/v1',
    
    # TTS 配置
    tts_engine='edge',
    tts_voice='zh-CN-XiaoxiaoNeural'
)

try:
    assistant.chat_loop()
finally:
    assistant.cleanup()
```

## 📚 详细文档

### 核心模块

#### 1. VoiceAssistant (主控制器)

主要的语音助手类，整合所有功能。

```python
from ai_voice_assistant import VoiceAssistant

assistant = VoiceAssistant(
    stt_engine='sphinx',
    stt_language='zh-CN',
    ai_api_key='your-api-key',
    ai_model='gpt-3.5-turbo',
    tts_engine='edge',
    tts_voice='zh-CN-XiaoxiaoNeural'
)
```

**主要方法:**

- `chat_once(listen_method='once')` - 进行一次对话
- `chat_loop(listen_method='once')` - 持续对话循环
- `chat_streaming(listen_method='once')` - 流式对话模式（边说边播）
- `stop()` - 停止对话
- `clear_history()` - 清空对话历史
- `set_system_prompt(prompt)` - 设置系统提示词
- `set_voice(voice)` - 设置 TTS 语音
- `set_rate(rate)` - 设置语速
- `set_volume(volume)` - 设置音量

#### 2. STTEngine (语音识别)

独立的语音识别引擎。

```python
from ai_voice_assistant import STTEngine

stt = STTEngine(
    engine='sphinx',  # 或 'whisper'
    language='zh-CN'
)

# 识别一次
text = stt.listen_once()

# 使用静音检测
text = stt.listen_with_silence_detection()

stt.cleanup()
```

#### 3. AIClient (AI 对话)

独立的 AI 对话客户端。

```python
from ai_voice_assistant import AIClient

ai = AIClient(
    api_key='your-api-key',
    model='gpt-3.5-turbo',
    api_base_url='https://api.openai.com/v1'
)

# 发送消息
response = ai.chat("你好")

# 流式输出
def on_chunk(chunk):
    print(chunk, end='', flush=True)

ai.set_on_message_callback(on_chunk)
response = ai.chat("你好", stream=True)
```

#### 4. TTSEngine (语音合成)

独立的语音合成引擎。

```python
from ai_voice_assistant import TTSEngine

tts = TTSEngine(
    engine='edge',
    voice='zh-CN-XiaoxiaoNeural'
)

# 朗读文字
tts.speak("你好，世界！")

# 保存到文件
tts.save_to_file("你好，世界！", "output.mp3")

tts.cleanup()
```

## 🔧 配置选项

### 支持的 AI 服务提供商

| 提供商 | 说明 | API 获取 |
|--------|------|----------|
| OpenAI | 最流行的 AI 服务 | https://platform.openai.com |
| 智谱AI | 国内优秀的 AI 服务 | https://open.bigmodel.cn |
| DeepSeek | 高性价比 AI 服务 | https://platform.deepseek.com |
| Ollama | 本地部署（免费） | https://ollama.ai |

### 语音识别引擎

| 引擎 | 类型 | 优点 | 缺点 |
|------|------|------|------|
| Sphinx | 离线 | 免费、无需网络 | 准确率一般 |
| Whisper | 在线 | 准确率高 | 需要网络 |

### 语音合成引擎

| 引擎 | 类型 | 优点 | 缺点 |
|------|------|------|------|
| Edge TTS | 在线 | 语音自然、流畅 | 需要网络 |
| pyttsx3 | 离线 | 无需网络 | 语音机械 |

## 🌐 如何集成到你的 App

### 方式 1: 直接复制模块

将 `ai_voice_assistant` 文件夹复制到你的项目中：

```bash
cp -r ai_voice_assistant /path/to/your/project/
```

然后在你的代码中导入：

```python
from ai_voice_assistant import VoiceAssistant
```

### 方式 2: 作为包安装（推荐）

在项目根目录运行：

```bash
pip install -e .
```

然后在任何地方使用：

```python
from ai_voice_assistant import VoiceAssistant
```

### 方式 3: 嵌入到现有代码

只使用你需要的模块：

```python
# 只使用语音识别
from ai_voice_assistant.stt_engine import STTEngine
stt = STTEngine()
text = stt.listen_once()

# 只使用 AI 对话
from ai_voice_assistant.ai_client import AIClient
ai = AIClient(api_key='your-key')
response = ai.chat('你好')

# 只使用语音合成
from ai_voice_assistant.tts_engine import TTSEngine
tts = TTSEngine()
tts.speak('你好')
```

## 📖 示例代码

查看 `examples.py` 文件，包含多个详细示例：

1. 基础使用
2. 自定义配置
3. 流式对话模式
4. 使用回调函数
5. 使用本地 Ollama
6. 动态修改设置

运行示例：

```bash
python examples.py
```

## 🎯 常见问题

### Q1: 安装 pyaudio 失败？

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Windows:**
通常直接 `pip install pyaudio` 即可。

### Q2: 如何获取 API key？

- **OpenAI**: https://platform.openai.com/api-keys
- **智谱AI**: https://open.bigmodel.cn/usercenter/apikeys
- **DeepSeek**: https://platform.deepseek.com/

### Q3: 如何使用离线模式？

使用 Sphinx 进行离线识别，pyttsx3 进行离线合成：

```python
assistant = VoiceAssistant(
    stt_engine='sphinx',  # 离线识别
    tts_engine='pyttsx3',  # 离线合成
    ai_api_key='your-key'
)
```

### Q4: 如何更改语音？

Edge TTS 支持多种语音，运行以下命令查看：

```python
from ai_voice_assistant import TTSEngine
tts = TTSEngine()
tts.list_voices()
```

常用中文语音：
- `zh-CN-XiaoxiaoNeural` (女声，温柔)
- `zh-CN-YunxiNeural` (男声，专业)
- `zh-CN-YunyangNeural` (男声，活泼)

### Q5: 如何提高识别准确率？

1. 使用 Whisper 引擎（需要网络）
2. 确保环境安静
3. 调整 `SILENCE_THRESHOLD` 参数

```python
assistant = VoiceAssistant(
    stt_engine='whisper',  # 使用 Whisper
    stt_language='zh-CN'
)
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题或建议，欢迎反馈。

---

**祝你使用愉快！** 🎉
