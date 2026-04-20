@echo off
chcp 65001 >nul

REM 中医智能诊断平台 - Windows启动脚本

echo 🚀 中医智能诊断平台 - 后端启动
echo ==================================

REM 检查Python
python --version
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查是否存在虚拟环境
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📥 安装依赖包...
pip install -r requirements.txt

REM 启动服务器
echo ✅ 启动后端服务...
echo 📍 API地址: http://localhost:8000
echo 📚 API文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

python app.py

pause
