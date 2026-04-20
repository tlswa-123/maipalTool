# 🚀 快速启动指南

## 一键启动（macOS/Linux）

```bash
# 1. 进入后端目录
cd backend

# 2. 给脚本添加执行权限
chmod +x start.sh

# 3. 启动后端
./start.sh
```

等待看到 "Uvicorn running on http://localhost:8000" 消息。

然后在另一个终端：

```bash
# 4. 启动前端服务器
python3 -m http.server 8001

# 5. 打开浏览器访问
open http://localhost:8001
```

## 一键启动（Windows）

```bash
# 1. 进入后端目录
cd backend

# 2. 双击运行
start.bat
```

等待看到 "Uvicorn running on http://localhost:8000" 消息。

然后在新的命令行窗口：

```bash
# 3. 启动前端服务器
python -m http.server 8001

# 4. 打开浏览器访问
start http://localhost:8001
```

## 测试API是否正常

在浏览器中访问：http://localhost:8000/docs

应该能看到Swagger API文档界面。

## 上传测试图片

1. 打开 http://localhost:8001
2. 选择"面诊"或"舌诊"
3. 上传一张清晰的照片
4. 点击"开始分析"
5. 等待2-3秒查看结果

## 常见问题

### 1. Python未安装

下载安装：https://www.python.org/downloads/

### 2. 后端启动失败

检查Python版本（需要3.8+）：
```bash
python3 --version
```

### 3. 前端连接不上后端

确保后端运行在 http://localhost:8000

### 4. 图片分析失败

确保上传清晰的正面照片，光线充足。

## 下一步

- 查看 README.md 了解详细功能
- 访问 http://localhost:8000/docs 测试API
- 查看 backend/face_diagnosis.py 了解实现细节

## 系统要求

- Python 3.8 或更高版本
- 4GB RAM 或更多
- 支持现代浏览器（Chrome、Firefox、Safari、Edge）
