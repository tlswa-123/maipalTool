# 项目结构

```
中医智能诊断平台/
├── index.html                      # 前端主页面
├── styles.css                      # 前端样式
├── app.js                         # 前端JavaScript（含模拟和真实AI模式）
├── README.md                      # 项目文档
├── QUICKSTART.md                   # 快速启动指南
├── PROJECT_STRUCTURE.md            # 本文件
├── .gitignore                     # Git忽略配置
│
├── backend/                       # 后端目录
│   ├── app.py                     # FastAPI主应用
│   ├── face_diagnosis.py           # 面诊分析模块
│   ├── tongue_diagnosis.py         # 舌诊分析模块
│   ├── test_api.py               # API测试脚本
│   ├── requirements.txt            # Python依赖
│   ├── .env                     # 环境配置
│   ├── start.sh                  # macOS/Linux启动脚本
│   └── start.bat                # Windows启动脚本
│
├── test_images/                  # 测试图片目录
│   └── README.md                # 测试图片说明
│
└── .workbuddy/                  # WorkBuddy工作目录（自动生成）
    └── memory/                  # 记忆文件
        └── 2026-04-05.md       # 每日记录
```

## 目录说明

### 前端文件
- `index.html` - 单页应用的主HTML文件
- `styles.css` - 响应式CSS样式
- `app.js` - 包含完整的诊断逻辑，支持真实AI和模拟两种模式

### 后端文件
- `app.py` - FastAPI应用，提供RESTful API
- `face_diagnosis.py` - 使用MediaPipe和OpenCV实现的面诊分析
- `tongue_diagnosis.py` - 使用OpenCV实现的舌诊分析
- `test_api.py` - API功能测试脚本
- `requirements.txt` - 所有Python依赖包
- `.env` - 环境变量配置

### 启动脚本
- `start.sh` - macOS/Linux一键启动脚本
- `start.bat` - Windows一键启动脚本

### 测试相关
- `test_images/` - 存放测试图片的目录
- `README.md` - 测试图片使用说明

## 工作流程

### 开发环境
1. 修改代码
2. 后端：`cd backend && python app.py`
3. 前端：`python3 -m http.server 8001`
4. 访问：http://localhost:8001

### 生产部署
1. 构建前端（可选，可使用打包工具）
2. 部署后端（使用Docker或云服务）
3. 配置反向代理（Nginx）
4. 启动服务

## 技术栈

### 前端
- HTML5 + CSS3 + JavaScript (ES6+)
- Fetch API (HTTP请求)
- FormData (文件上传)

### 后端
- Python 3.8+
- FastAPI (Web框架)
- Uvicorn (ASGI服务器)
- OpenCV (图像处理)
- MediaPipe (人脸检测)
- scikit-learn (机器学习)

## API端点

```
GET  /                         # API信息
GET  /health                   # 健康检查
POST /api/face/analyze        # 面诊分析
POST /api/tongue/analyze      # 舌诊分析
```

## 配置文件

### .env
```env
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=*
LOG_LEVEL=info
```

## 扩展方向

### 短期
- [ ] 添加用户认证
- [ ] 历史记录功能
- [ ] 图片预处理优化

### 中期
- [ ] 批量分析
- [ ] 数据统计和可视化
- [ ] 多语言支持

### 长期
- [ ] 移动端App
- [ ] 云端部署方案
- [ ] 深度学习模型训练
