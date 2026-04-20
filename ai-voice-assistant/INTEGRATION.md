# 集成指南 📦

本指南详细说明如何将 AI 语音助手集成到你的 App 中。

## 📋 前置准备

在集成之前，请确保：

1. ✅ 已安装 Python 3.8+
2. ✅ 已安装所需依赖（见 `requirements.txt`）
3. ✅ 已获取 AI 服务的 API key（或使用 Ollama）
4. ✅ 已测试麦克风和音箱正常工作

## 🎯 集成方式

### 方式 1: 完整集成（推荐）

适合需要完整语音对话功能的 App。

#### 步骤 1: 复制模块

将整个 `ai_voice_assistant` 文件夹复制到你的项目中：

```bash
cp -r ai_voice_assistant /path/to/your/project/
```

#### 步骤 2: 初始化助手

在你的主代码中：

```python
from ai_voice_assistant import VoiceAssistant

# 初始化助手
assistant = VoiceAssistant(
    stt_engine='sphinx',
    stt_language='zh-CN',
    ai_api_key='your-api-key',
    ai_model='gpt-3.5-turbo',
    tts_engine='edge',
    tts_voice='zh-CN-XiaoxiaoNeural'
)
```

#### 步骤 3: 启动对话

```python
try:
    # 启动对话循环
    assistant.chat_loop()
except KeyboardInterrupt:
    pass
finally:
    assistant.cleanup()
```

#### 步骤 4: 与你的 App 集成

你可以通过回调函数与你的 App 交互：

```python
# 设置回调函数
def on_recognized(text):
    """识别完成时调用"""
    print(f"识别到: {text}")
    # 在这里更新你的 UI 或执行其他操作
    # 例如: app.update_ui(text)

def on_ai_response(response):
    """AI 回复时调用"""
    print(f"AI 回复: {response}")
    # 在这里更新你的 UI 或执行其他操作
    # 例如: app.show_ai_message(response)

def on_error(error):
    """发生错误时调用"""
    print(f"错误: {error}")
    # 在这里显示错误信息
    # 例如: app.show_error(error)

# 注册回调
assistant.set_on_recognized_callback(on_recognized)
assistant.set_on_ai_response_callback(on_ai_response)
assistant.set_on_error_callback(on_error)
```

### 方式 2: 分模块集成

适合只需要部分功能的 App。

#### 只使用语音识别 (STT)

```python
from ai_voice_assistant.stt_engine import STTEngine

# 创建 STT 引擎
stt = STTEngine(
    engine='sphinx',
    language='zh-CN'
)

# 在你的 App 中调用
def on_record_button_clicked():
    """当用户点击录音按钮时"""
    text = stt.listen_once()
    if text:
        # 处理识别到的文字
        process_text(text)

# 清理
stt.cleanup()
```

#### 只使用 AI 对话

```python
from ai_voice_assistant.ai_client import AIClient

# 创建 AI 客户端
ai = AIClient(
    api_key='your-api-key',
    model='gpt-3.5-turbo'
)

# 在你的 App 中调用
def on_send_message(user_input):
    """当用户发送消息时"""
    response = ai.chat(user_input)
    # 显示 AI 回复
    show_response(response)
```

#### 只使用语音合成 (TTS)

```python
from ai_voice_assistant.tts_engine import TTSEngine

# 创建 TTS 引擎
tts = TTSEngine(
    engine='edge',
    voice='zh-CN-XiaoxiaoNeural'
)

# 在你的 App 中调用
def on_ai_response(response):
    """当 AI 回复时"""
    # 显示文字
    show_text(response)
    # 同时播放语音
    tts.speak(response, blocking=False)

# 清理
tts.cleanup()
```

### 方式 3: Web 应用集成

如果是 Web 应用，推荐使用 WebSocket 实现实时对话。

#### 后端 (Python + FastAPI)

```python
from fastapi import FastAPI, WebSocket
from ai_voice_assistant import VoiceAssistant
import asyncio

app = FastAPI()
assistant = VoiceAssistant(
    stt_engine='sphinx',
    ai_api_key='your-api-key',
    tts_engine='edge'
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 接收客户端消息
            data = await websocket.receive_text()
            
            # AI 对话
            response = assistant.ai.chat(data)
            
            # 发送回复
            await websocket.send_text(response)
            
    finally:
        assistant.cleanup()
```

#### 前端 (JavaScript)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

// 发送消息
function sendMessage(text) {
    ws.send(text);
}

// 接收消息
ws.onmessage = (event) => {
    const response = event.data;
    // 显示 AI 回复
    displayResponse(response);
    // 播放语音（使用浏览器 TTS）
    speak(response);
};

// 浏览器 TTS
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    speechSynthesis.speak(utterance);
}
```

### 方式 4: 移动应用集成

#### iOS (Swift)

```swift
import Foundation

class VoiceAssistantManager {
    private var assistant: VoiceAssistant
    
    init(apiKey: String) {
        // 通过 Python 桥接调用
        self.assistant = VoiceAssistant(
            ai_api_key: apiKey,
            stt_engine: 'sphinx',
            tts_engine: 'edge'
        )
    }
    
    func startVoiceRecognition(completion: @escaping (String?) -> Void) {
        DispatchQueue.global(qos: .userInitiated).async {
            let text = self.assistant.stt.listen_once()
            DispatchQueue.main.async {
                completion(text)
            }
        }
    }
    
    func getAIResponse(for text: String, completion: @escaping (String) -> Void) {
        DispatchQueue.global(qos: .userInitiated).async {
            let response = self.assistant.ai.chat(text)
            DispatchQueue.main.async {
                completion(response)
            }
        }
    }
}
```

#### Android (Kotlin)

```kotlin
import kotlinx.coroutines.*

class VoiceAssistantManager(private val apiKey: String) {
    private val assistant = VoiceAssistant(
        ai_api_key = apiKey,
        stt_engine = "sphinx",
        tts_engine = "edge"
    )
    
    fun startVoiceRecognition(onResult: (String?) -> Unit) {
        CoroutineScope(Dispatchers.IO).launch {
            val text = assistant.stt.listenOnce()
            withContext(Dispatchers.Main) {
                onResult(text)
            }
        }
    }
    
    fun getAIResponse(text: String, onResponse: (String) -> Unit) {
        CoroutineScope(Dispatchers.IO).launch {
            val response = assistant.ai.chat(text)
            withContext(Dispatchers.Main) {
                onResponse(response)
            }
        }
    }
}
```

## 🔧 高级集成技巧

### 1. 自定义系统提示词

根据你的 App 类型，设置合适的系统提示词：

```python
# 客服助手
assistant.set_system_prompt(
    "你是一个专业的客服助手，请用礼貌、专业的语言回答用户问题。"
)

# 教育助手
assistant.set_system_prompt(
    "你是一个教育助手，请用简单易懂的语言解释复杂的概念。"
)

# 娱乐助手
assistant.set_system_prompt(
    "你是一个幽默风趣的AI助手，请用轻松的语气回答问题，可以适当开玩笑。"
)
```

### 2. 实现打断功能

允许用户在 AI 说话时打断：

```python
is_speaking = False

def on_ai_response(response):
    global is_speaking
    is_speaking = True
    tts.speak(response, blocking=False)
    is_speaking = False

def on_recognized(text):
    if is_speaking:
        # 如果正在说话，先停止
        tts.stop_recording()
    # 重新开始对话
    process_new_dialogue(text)
```

### 3. 添加快捷指令

实现常用快捷词，快速执行操作：

```python
shortcuts = {
    '打开': open_feature,
    '关闭': close_feature,
    '搜索': search_feature,
    '返回': go_back,
}

def on_recognized(text):
    # 检查是否是快捷指令
    for keyword, action in shortcuts.items():
        if keyword in text:
            action(text)
            return
    
    # 如果不是快捷指令，发送给 AI
    response = assistant.ai.chat(text)
    on_ai_response(response)
```

### 4. 上下文管理

根据场景调整 AI 行为：

```python
# 定义不同的场景
contexts = {
    'default': '你是一个通用的AI助手。',
    'navigation': '你是一个导航助手，专注于提供路线和交通信息。',
    'shopping': '你是一个购物助手，专注于商品推荐和购买建议。',
}

def switch_context(context_name):
    assistant.set_system_prompt(contexts.get(context_name, contexts['default']))

# 切换到导航模式
switch_context('navigation')
```

### 5. 错误处理和重试

```python
def chat_with_retry(max_retries=3):
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            success, user_text, ai_response = assistant.chat_once()
            
            if success:
                return ai_response
            else:
                retry_count += 1
                print(f"重试 {retry_count}/{max_retries}")
                time.sleep(1)
                
        except Exception as e:
            retry_count += 1
            print(f"错误: {e}, 重试 {retry_count}/{max_retries}")
            time.sleep(1)
    
    return "抱歉，我现在无法回答，请稍后再试。"
```

## 📱 完整示例项目结构

```
your_app/
├── ai_voice_assistant/          # 语音助手模块
│   ├── __init__.py
│   ├── voice_assistant.py
│   ├── stt_engine.py
│   ├── ai_client.py
│   ├── tts_engine.py
│   └── config.py
├── main.py                     # 你的主程序
├── ui/                         # UI 相关
│   ├── __init__.py
│   └── interface.py
├── requirements.txt
└── config/
    └── settings.py
```

## ✅ 集成检查清单

集成完成后，请检查以下项目：

- [ ] 语音识别能正确识别用户的语音
- [ ] AI 能正确理解并回复用户的问题
- [ ] 语音合成能正确播放 AI 的回复
- [ ] 所有回调函数正常工作
- [ ] 错误处理完善
- [ ] 资源正确清理（调用 `cleanup()`）
- [ ] 在你的 App 中 UI 正常更新
- [ ] 性能良好，无明显延迟

## 🆘 获取帮助

如果遇到集成问题：

1. 查看 `README.md` 中的常见问题
2. 查看 `examples.py` 中的示例代码
3. 运行各个模块的测试代码（在 `__main__` 中）
4. 检查日志输出，定位问题

---

祝你集成顺利！🎉
