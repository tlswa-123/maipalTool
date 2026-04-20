# 🚀 5 分钟快速开始

按照这个指南，5 分钟内就能让你的 AI 语音助手跑起来！

## 步骤 1: 安装依赖 ⏱️ 2 分钟

### Windows

```bash
# 双击运行安装脚本
install.bat
```

### macOS/Linux

```bash
# 添加执行权限
chmod +x install.sh

# 运行安装脚本
./install.sh
```

或者手动安装：

```bash
pip install -r requirements.txt
```

## 步骤 2: 配置 API ⏱️ 1 分钟

### 选项 A: 使用免费服务（推荐新手）

使用 Ollama 本地模型（完全免费）：

```bash
# 安装 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 下载模型
ollama pull llama2

# 启动服务
ollama serve
```

### 选项 B: 使用付费服务

获取 API key：

- **智谱AI**: https://open.bigmodel.cn/usercenter/apikeys (有免费额度)
- **DeepSeek**: https://platform.deepseek.com/ (有免费额度)
- **OpenAI**: https://platform.openai.com/api-keys (需要付费)

配置环境变量：

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API key
# API_KEY=your-api-key-here
```

## 步骤 3: 运行测试 ⏱️ 2 分钟

### 方式 1: 使用快速启动脚本（最简单）

```bash
python quick_start.py
```

脚本会：
1. 自动检查依赖
2. 交互式选择 AI 服务
3. 启动语音助手
4. 你可以开始对话！

### 方式 2: 运行示例

```bash
# 编辑 examples.py，选择你要运行的示例
python examples.py
```

### 方式 3: 直接在代码中使用

创建一个新文件 `test.py`：

```python
from ai_voice_assistant import VoiceAssistant

# 使用 Ollama（本地，免费）
assistant = VoiceAssistant(
    stt_engine='sphinx',
    ai_api_key='ollama',
    ai_model='llama2',
    ai_api_base='http://localhost:11434/v1',
    tts_engine='edge',
    tts_voice='zh-CN-XiaoxiaoNeural'
)

# 开始对话
assistant.chat_loop()

# 清理资源
assistant.cleanup()
```

运行：

```bash
python test.py
```

## 步骤 4: 开始对话！🎉

对着麦克风说话，AI 会：
1. 🔊 识别你的语音
2. 🤖 思考并生成回复
3. 🔊 同时播放语音和显示文字

## 常见问题

### Q1: 安装 PyAudio 失败？

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Windows:**
通常直接安装即可。如果失败，尝试：
```bash
pip install pipwin
pipwin install pyaudio
```

### Q2: 麦克风无法使用？

检查系统设置：
- macOS: 系统设置 → 声音 → 输入
- Windows: 设置 → 系统 → 声音 → 输入
- Linux: `pavucontrol` 或 `alsamixer`

### Q3: 无法识别语音？

确保：
- 麦克风已连接
- 麦克音量已打开
- 环境不要太吵
- 说话清晰一点

### Q4: AI 没有回复？

检查：
- API key 是否正确
- 网络是否连接
- API 配额是否用完
- 查看错误日志

### Q5: 语音不自然？

尝试不同的声音：

```python
# 在代码中设置
assistant.set_voice('zh-CN-YunxiNeural')  # 男声
assistant.set_voice('zh-CN-XiaoxiaoNeural')  # 女声
```

或者运行代码查看所有可用声音：

```python
from ai_voice_assistant import TTSEngine
tts = TTSEngine()
tts.list_voices()
```

## 下一步

### 📚 学习更多

- 查看完整文档: `README.md`
- 了解如何集成: `INTEGRATION.md`
- 查看更多示例: `examples.py`

### 🔧 自定义配置

编辑 `.env` 文件或直接在代码中配置：

```python
assistant = VoiceAssistant(
    # STT 配置
    stt_engine='whisper',  # 使用更准确的识别
    stt_language='zh-CN',
    
    # AI 配置
    ai_api_key='your-key',
    ai_model='gpt-4',  # 使用更好的模型
    ai_system_prompt='你是一个专业的客服助手。',
    
    # TTS 配置
    tts_engine='edge',
    tts_voice='zh-CN-XiaoxiaoNeural',
    tts_rate=120,  # 语速
    tts_volume=80  # 音量
)
```

### 🌟 高级功能

- **流式对话**: 边说边播
- **回调函数**: 与你的 App 集成
- **快捷指令**: 快速执行操作
- **多语言**: 支持英文、日文等

## 🎯 快速命令参考

```bash
# 安装依赖
pip install -r requirements.txt

# 运行快速启动
python quick_start.py

# 运行示例
python examples.py

# 测试语音识别
python -m ai_voice_assistant.stt_engine

# 测试 AI 对话
python -m ai_voice_assistant.ai_client

# 测试语音合成
python -m ai_voice_assistant.tts_engine
```

---

**恭喜！你的 AI 语音助手已经准备好了！** 🎉

有问题？查看 `README.md` 或 `INTEGRATION.md` 获取更多帮助。
