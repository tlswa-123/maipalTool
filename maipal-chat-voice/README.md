# maipal-chat-voice

脉大夫中医问诊 Web 端——集成 **语音输入（STT）**、**语音朗读（TTS）**、**望诊**（面部 / 舌部）、**闻诊**（语声 + 节奏）。

## 📐 与仓库其他目录的关系

- `maipai-chat-v2/` — 脉大夫对话的**原始纯文字版本**（上一代）
- `ai-voice-assistant/` — 独立 Python 语音助手模块
- `tcm-diagnosis-platform/` — **望诊后端**（面诊 / 舌诊），提供 `/api/face/analyze`、`/api/tongue/analyze`
- `maipal-chat-voice/` — **本目录**：在 `maipai-chat-v2` 基础上叠加了 STT/TTS、摄像头望诊、麦克风闻诊；对话后端作为统一网关，把望闻诊请求代理到 `tcm-diagnosis-platform`

## 🧱 架构

```
┌────────────────────────────────────────────────┐
│                  浏览器前端                     │
│   public/index.html                            │
│   · 对话 UI + 流式渲染                          │
│   · Web Speech API 做语音输入                   │
│   · speechSynthesis 做 TTS 朗读                 │
│   · 摄像头（拍面/舌） + MediaStream（录音）     │
│   · 监听 AI 消息里的 ```tool_call``` 信号         │
└─────────────────────────┬──────────────────────┘
                          │ HTTP
┌─────────────────────────▼──────────────────────┐
│         脉大夫对话后端  server.js  (3215)       │
│   · /api/opening     开场白                    │
│   · /api/chat        流式对话（转发 Claw API） │
│   · /api/diagnosis/* 望闻诊代理（见下）        │
└─────────────────────────┬──────────────────────┘
                          │ HTTP 127.0.0.1:8000
┌─────────────────────────▼──────────────────────┐
│  tcm-diagnosis-platform/backend  app.py (8000) │
│   · /api/face/analyze    面诊 MediaPipe+OpenCV │
│   · /api/tongue/analyze  舌诊 MediaPipe+OpenCV │
│   · /api/voice/analyze   闻诊 Parselmouth/Praat│
└────────────────────────────────────────────────┘
```

## 📂 目录结构

```
maipal-chat-voice/
├── server.js           # 脉大夫对话后端（Node.js）
├── package.json
├── persona.md          # 脉大夫 system prompt（含信号协议）
├── public/
│   └── index.html      # 前端：对话 + 望闻诊 + STT/TTS
└── backend-patch/      # 对 tcm-diagnosis-platform/backend 的增量
    ├── app.py          # 在原 app.py 基础上挂载 /api/voice/analyze
    └── voice_diagnosis.py   # 闻诊分析器（Parselmouth）
```

⚠️ `backend-patch/` 用于**增量更新 `tcm-diagnosis-platform/backend/`**。使用时把 `app.py` 覆盖原目录里的同名文件、把 `voice_diagnosis.py` 新增进去即可。不要直接改动原 `tcm-diagnosis-platform` 目录结构。

## 🚀 启动步骤

### 1) 望闻诊后端（tcm-diagnosis-platform）

```bash
# 合并 patch
cp maipal-chat-voice/backend-patch/voice_diagnosis.py tcm-diagnosis-platform/backend/
cp maipal-chat-voice/backend-patch/app.py            tcm-diagnosis-platform/backend/

# 装依赖
cd tcm-diagnosis-platform/backend
pip install -r requirements.txt
pip install praat-parselmouth    # 新依赖：闻诊用

# 启动
python3 app.py                   # http://localhost:8000
```

### 2) 脉大夫对话后端（本目录）

```bash
cd maipal-chat-voice
export CODEBUDDY_API_KEY=你的腾讯 CodeBuddy Key
node server.js                   # http://localhost:3215
```

浏览器打开 http://localhost:3215 即可。

## 🛰️ 信号协议

AI 会在消息末尾追加一段 ```tool_call``` 代码块，前端解析后唤起对应设备：

| action | 设备 | 回传字段 |
|---|---|---|
| `CAPTURE_FACE`   | 摄像头 | `facial_diagnosis` + `tcm_diagnosis` |
| `CAPTURE_TONGUE` | 摄像头 | `tongue_diagnosis` + `tcm_diagnosis` |
| `RECORD_VOICE`   | 麦克风 | `voice_diagnosis` + `tcm_diagnosis` |
| `GENERATE_REPORT` | —     | AI 在消息正文中直接给出报告 |

信号 JSON 示例：

```json
{"action": "RECORD_VOICE", "reason": "闻语声与气息", "guidance": "请朗读：'今天来看看我这身体情况'"}
```

详见 `persona.md`「一·附：系统信号协议」章节。

## 🔐 安全说明

- `server.js` **不包含** API Key，需要通过 `CODEBUDDY_API_KEY` 环境变量提供
- 所有分析都在本地 127.0.0.1 调用，不走外网
- 图像 / 音频仅内存中临时处理，分析完即释放

## 📦 依赖

**Node 端**：纯原生 `http/https`，无外部 npm 依赖。

**Python 端（tcm-diagnosis-platform）**：
- `fastapi`, `uvicorn`, `python-multipart`
- `opencv-python-headless`, `mediapipe`, `numpy`, `scikit-learn`（望诊）
- `praat-parselmouth`（闻诊）
- 可选：`ffmpeg`（非 WAV 格式解码；当前前端直接上传 WAV，可免装）

## 📄 License

参考主仓库 LICENSE。本目录中的 `praat-parselmouth` 是 GPL-3.0，但仅在服务器端使用（SaaS 模式）不构成分发。
