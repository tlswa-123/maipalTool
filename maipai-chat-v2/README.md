# 脉大夫中医问诊系统

基于 WorkBuddy/CodeBuddy API 的中医 AI 问诊网页应用。

## 项目结构

```
maipai-chat/
├── server.js          # Node.js 后端服务（代理 API + 流式响应）
├── persona.md         # 脉大夫角色设定和中医知识库文档
├── public/
│   └── index.html     # 前端问诊界面
├── package.json       # 项目配置
└── README.md          # 使用说明
```

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置 API Key

编辑 `server.js`，将 `apiKey` 替换为你的 CodeBuddy API Key：

```javascript
const CONFIG = {
  port: 3210,
  apiEndpoint: 'copilot.tencent.com',
  apiPath: '/v2/chat/completions',
  apiKey: '你的_API_Key_这里'  // <-- 替换这里
};
```

### 3. 启动服务

```bash
npm start
```

或

```bash
node server.js
```

### 4. 打开网页

浏览器访问 http://localhost:3210

## 功能特性

- 🧑‍⚕️ **脉大夫人设**：资深中医师角色，温和亲切
- 🎯 **目标人群**：45-65岁中老年人，养生调理为主
- 💬 **对话方式**：一次只问一个问题，像真人面对面
- 📝 **问诊流程**：遵循中医十问歌，从问称呼开始
- 🔄 **流式回复**：逐字显示，体验流畅
- 📋 **导出记录**：一键导出问诊记录为 Markdown
- 🎨 **中医风格**：暖色调界面设计

## 技术栈

- **后端**：Node.js (原生 http/https，零依赖)
- **前端**：纯 HTML/CSS/JavaScript (无框架)
- **API**：CodeBuddy/WorkBuddy (copilot.tencent.com)
- **流式**：Server-Sent Events (SSE)

## 人设文档

`persona.md` 包含完整的：
- AI 角色设定（System Prompt）
- 中医知识库架构（14学科23个JSON）
- 问诊对话流程设计
- 诊断报告模板
- 问诊开场白

## 许可证

MIT
