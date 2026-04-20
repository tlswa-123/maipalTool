# 🔧 AI 语音助手 Web 应用 - 故障排除指南

## 问题：AI 生成错误

### 可能的原因和解决方案

#### 1. API Key 错误

**症状：**
- 点击"发送给 AI"后显示错误
- 错误信息包含 "API Key" 或 "authentication"

**解决方案：**
1. **检查 API Key 是否正确**
   - 确保没有多余的空格
   - 确认 API Key 是否完整复制
   - 检查是否使用了正确的 API Key

2. **检查 API Key 是否有效**
   - 登录对应的 AI 服务平台
   - 查看余额是否充足
   - 确认 API Key 是否已激活

3. **重新获取 API Key**
   - OpenAI: https://platform.openai.com/api-keys
   - 智谱 AI: https://open.bigmodel.cn/usercenter/apikeys
   - DeepSeek: https://platform.deepseek.com/

---

#### 2. 网络连接问题

**症状：**
- 请求超时
- 连接错误
- 502/504 错误

**解决方案：**
1. **检查网络连接**
   ```bash
   ping api.openai.com
   ping open.bigmodel.cn
   ```

2. **检查代理设置**
   - 如果使用了代理，确保代理配置正确
   - 尝试关闭代理

3. **使用本地 Ollama**
   ```bash
   # 安装 Ollama
   curl -fsSL https://ollama.ai/install.sh | sh

   # 下载模型
   ollama pull llama2

   # 启动服务
   ollama serve
   ```

---

#### 3. 模型名称错误

**症状：**
- 错误信息包含 "model" 或 "模型"

**解决方案：**
1. **检查模型名称是否正确**
   - OpenAI: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`
   - 智谱 AI: `glm-4`, `glm-3-turbo`
   - DeepSeek: `deepseek-chat`, `deepseek-coder`
   - Ollama: `llama2`, `mistral`, `codellama`

2. **确认模型是否可用**
   - 登录对应的 AI 服务平台
   - 查看可用模型列表

---

#### 4. 请求格式错误

**症状：**
- 400 错误
- "Bad Request" 错误

**解决方案：**
1. **检查请求参数**
   - 确保所有必填参数都已提供
   - 检查参数格式是否正确

2. **查看详细错误日志**
   ```bash
   tail -f /Users/tlswa/WorkBuddy/20260325232824/web_app/app.log
   ```

---

#### 5. 服务器错误

**症状：**
- 500 错误
- "Internal Server Error"

**解决方案：**
1. **查看服务器日志**
   ```bash
   tail -n 50 /Users/tlswa/WorkBuddy/20260325232824/web_app/app.log
   ```

2. **重启服务器**
   ```bash
   pkill -f simple_app.py
   cd /Users/tlswa/WorkBuddy/20260325232824/web_app
   nohup python3 simple_app.py > app.log 2>&1 &
   ```

3. **检查依赖是否安装**
   ```bash
   pip3 list | grep -E "(Flask|requests|edge-tts)"
   ```

---

## 🧪 测试步骤

### 测试 1: 健康检查

```bash
curl http://localhost:5000/api/health
```

**预期结果：**
```json
{
  "status": "ok",
  "ai_instances": 0,
  "tts_initialized": false
}
```

---

### 测试 2: AI 对话（使用 Ollama）

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "provider": "ollama",
    "model": "llama2",
    "system_prompt": "你是一个友好的AI助手。"
  }'
```

**预期结果：**
```json
{
  "success": true,
  "response": "你好！有什么可以帮助你的吗？",
  "provider": "ollama",
  "model": "llama2"
}
```

---

### 测试 3: AI 对话（使用智谱 AI）

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "provider": "zhipu",
    "model": "glm-4",
    "api_key": "your-api-key-here",
    "system_prompt": "你是一个友好的AI助手。"
  }'
```

---

### 测试 4: 语音合成

```bash
curl -X POST http://localhost:5000/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好，这是一个测试。",
    "engine": "edge",
    "voice": "zh-CN-XiaoxiaoNeural"
  }'
```

**预期结果：**
```json
{
  "success": true,
  "audio_url": "/audio/tts_1774533421883.mp3",
  "engine": "edge"
}
```

---

## 📝 常见错误信息及解决方案

### 错误 1: `AttributeError: module 'os' has no attribute 'time'`

**原因：** 代码错误，使用了 `os.time()` 而不是 `time.time()`

**解决方案：** 已经修复，重启应用即可

```bash
pkill -f simple_app.py
cd /Users/tlswa/WorkBuddy/20260325232824/web_app
nohup python3 simple_app.py > app.log 2>&1 &
```

---

### 错误 2: `404 Not Found`

**原因：** 路由不存在或服务器未启动

**解决方案：**
1. 检查服务器是否运行
   ```bash
   ps aux | grep simple_app.py
   ```

2. 检查端口是否正确
   ```bash
   lsof -i :5000
   ```

---

### 错误 3: `Connection refused`

**原因：** 服务器未启动或端口被占用

**解决方案：**
1. 检查服务器是否运行
   ```bash
   ps aux | grep simple_app.py
   ```

2. 如果端口被占用，更换端口
   ```python
   # 在 simple_app.py 中修改
   app.run(
       host='0.0.0.0',
       port=5001,  # 改为其他端口
       debug=True
   )
   ```

---

### 错误 4: `ImportError: No module named 'edge_tts'`

**原因：** 依赖未安装

**解决方案：**
```bash
pip3 install edge-tts
```

---

### 错误 5: `ImportError: No module named 'flask'`

**原因：** 依赖未安装

**解决方案：**
```bash
pip3 install Flask Flask-Cors Werkzeug
```

---

## 🚀 快速修复清单

如果遇到 AI 生成错误，按以下顺序检查：

1. ✅ **检查 API Key**
   - 是否正确填入
   - 是否有余额
   - 是否已激活

2. ✅ **检查网络**
   - 是否能访问 AI 服务
   - 代理设置是否正确

3. ✅ **检查模型**
   - 模型名称是否正确
   - 模型是否可用

4. ✅ **查看日志**
   ```bash
   tail -f /Users/tlswa/WorkBuddy/20260325232824/web_app/app.log
   ```

5. ✅ **重启服务**
   ```bash
   pkill -f simple_app.py
   cd /Users/tlswa/WorkBuddy/20260325232824/web_app
   nohup python3 simple_app.py > app.log 2>&1 &
   ```

6. ✅ **测试 API**
   ```bash
   python3 test_api.py
   ```

---

## 📞 获取帮助

如果以上方法都无法解决问题：

1. **查看完整日志**
   ```bash
   tail -n 100 /Users/tlswa/WorkBuddy/20260325232824/web_app/app.log
   ```

2. **检查依赖**
   ```bash
   pip3 list
   ```

3. **重新安装依赖**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **查看文档**
   - README.md
   - WEB_GUIDE.md
   - TROUBLESHOOTING.md（本文件）

---

## 💡 推荐的测试顺序

### 1. 先测试文字输入（推荐智谱 AI 或 DeepSeek）

1. 在"设置"中配置智谱 AI 或 DeepSeek
2. 输入简单的文字，如"你好"
3. 点击"发送给 AI"
4. 查看是否正常回复

**为什么推荐智谱 AI 或 DeepSeek？**
- 有免费额度
- 价格便宜
- 响应速度快
- 中文支持好

### 2. 再测试语音识别

1. 点击"开始录音"
2. 说"你好"
3. 查看识别结果

### 3. 最后测试语音合成

1. 等待 AI 回复
2. 点击"播放语音"
3. 听 AI 语音

---

## 🎯 下一步

如果问题仍然存在：

1. **提供详细的错误信息**
   - 错误截图
   - 服务器日志
   - 配置信息（隐藏 API Key）

2. **提供测试步骤**
   - 使用的 AI 服务
   - API Key 类型
   - 输入的消息

3. **提供环境信息**
   - 操作系统
   - Python 版本
   - 依赖版本

---

**祝使用愉快！** 🎉
