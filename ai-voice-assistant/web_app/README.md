# 🌐 AI 语音助手 Web 应用

一个在线测试 AI 语音识别、AI 对话和语音合成的 Web 应用。

## 🚀 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问: **http://localhost:5000**

## ✨ 功能特性

### 🎤 语音识别 (STT)
- 支持在线录音
- 支持上传音频文件
- 两种识别引擎：Sphinx (离线) 和 Whisper (在线)
- 实时音量显示
- 音频可视化

### 🤖 AI 对话
- 支持多种 AI 服务：
  - OpenAI (GPT-3.5, GPT-4)
  - 智谱 AI (GLM-4, GLM-3 Turbo)
  - DeepSeek (DeepSeek Chat)
  - Ollama (本地模型，免费)
- 自定义系统提示词
- 实时对话

### 🔊 语音合成 (TTS)
- 两种合成引擎：Edge TTS (在线) 和 pyttsx3 (离线)
- 多种语音可选
- 自然流畅的语音播放
- 支持保存音频文件

## 📋 使用说明

### 语音识别

1. 点击 **"开始录音"** 按钮
2. 对着麦克风说话
3. 点击 **"停止录音"** 按钮
4. 系统会自动识别并显示文字
5. 或直接在文本框中输入文字

### AI 对话

1. 在用户输入框中输入文字
2. 点击 **"发送给 AI"** 按钮
3. AI 会生成回复并显示

### 语音合成

1. 获取 AI 回复后
2. 点击 **"播放语音"** 按钮
3. 系统会播放 AI 的语音

### 配置设置

在设置面板中可以配置：

- **语音识别引擎**: Sphinx (离线) 或 Whisper (在线)
- **AI 服务提供商**: OpenAI、智谱AI、DeepSeek、Ollama
- **AI 模型**: 根据提供商选择不同模型
- **API Key**: 填入你的 API Key (Ollama 不需要)
- **语音合成引擎**: Edge TTS (在线) 或 pyttsx3 (离线)
- **TTS 语音**: 选择喜欢的语音
- **系统提示词**: 自定义 AI 的人设

## 🔑 获取 API Key

### OpenAI
https://platform.openai.com/api-keys

### 智谱 AI
https://open.bigmodel.cn/usercenter/apikeys

### DeepSeek
https://platform.deepseek.com/

### Ollama (免费)
```bash
# 安装 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 下载模型
ollama pull llama2

# 启动服务
ollama serve
```

## 📡 API 端点

### POST /api/stt
语音识别

**请求:**
- 方法: POST
- Content-Type: multipart/form-data
- 参数:
  - audio: 音频文件
  - engine: 识别引擎 (sphinx/whisper)
  - language: 识别语言 (zh-CN/en-US)

**响应:**
```json
{
  "success": true,
  "text": "识别的文字",
  "engine": "sphinx"
}
```

### POST /api/chat
AI 对话

**请求:**
- 方法: POST
- Content-Type: application/json
- 参数:
  - message: 用户消息
  - provider: AI 提供商 (openai/zhipu/deepseek/ollama)
  - model: AI 模型
  - api_key: API Key
  - system_prompt: 系统提示词

**响应:**
```json
{
  "success": true,
  "response": "AI 的回复",
  "provider": "openai",
  "model": "gpt-3.5-turbo"
}
```

### POST /api/tts
语音合成

**请求:**
- 方法: POST
- Content-Type: application/json
- 参数:
  - text: 要合成的文字
  - engine: 合成引擎 (edge/pyttsx3)
  - voice: 语音名称

**响应:**
```json
{
  "success": true,
  "audio_url": "/audio/tts_xxx.mp3",
  "engine": "edge"
}
```

### GET /api/health
健康检查

**响应:**
```json
{
  "status": "ok",
  "stt_instances": 1,
  "ai_instances": 1,
  "tts_initialized": true
}
```

### POST /api/cleanup
清理资源

**响应:**
```json
{
  "success": true,
  "message": "资源已清理"
}
```

## 🛠️ 技术栈

### 后端
- Python 3.8+
- Flask - Web 框架
- Flask-CORS - 跨域支持

### 核心功能
- SpeechRecognition - 语音识别
- OpenAI API / 智谱 AI API / DeepSeek API / Ollama - AI 对话
- edge-tts / pyttsx3 - 语音合成

### 前端
- HTML5
- CSS3
- JavaScript (原生)
- Web Audio API - 音频处理
- MediaRecorder API - 录音功能

## 📝 项目结构

```
web_app/
├── app.py                # Flask 后端服务器
├── requirements.txt      # Python 依赖
├── README.md            # 本文件
├── templates/           # 前端模板
│   └── index.html      # 主页面
├── uploads/            # 上传的音频文件
└── audio_output/       # 生成的音频文件
```

## 🔧 配置

### 端口
默认端口: 5000

在 `app.py` 中修改:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### 最大上传大小
默认: 16MB

在 `app.py` 中修改:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
```

## 🐛 常见问题

### Q1: 无法访问麦克风？
**A:** 确保浏览器允许麦克风权限，并在 HTTPS 环境下运行（本地 localhost 可以）。

### Q2: 录音失败？
**A:** 检查麦克风是否正常工作，确保在支持的浏览器中运行（Chrome、Firefox、Edge）。

### Q3: 识别不准确？
**A:** 尝试使用 Whisper 引擎（需要网络），或在安静的环境中使用。

### Q4: AI 没有回复？
**A:** 检查 API Key 是否正确，网络是否连接，查看日志了解详细错误。

### Q5: 无法播放语音？
**A:** 确保浏览器支持音频播放，检查音频文件是否生成成功。

## 📱 浏览器支持

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Edge 79+
- ✅ Safari 14+

## 🔒 隐私说明

- 所有音频文件在处理后会被删除
- 生成的音频文件会在 1 小时后自动清理
- 不会保存任何对话历史

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**祝你使用愉快！** 🎉

有问题请查看主项目的 README.md 或提交 Issue。
