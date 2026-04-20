@echo off
chcp 65001 > nul
echo ============================================
echo 🚀 AI 语音助手 Web 应用启动脚本
echo ============================================
echo.

REM 检查 Python
echo 📦 检查 Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python 未安装或未添加到 PATH
    pause
    exit /b 1
)

REM 检查依赖
echo.
echo 📦 检查依赖...
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Flask 未安装
    echo 💡 请运行: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ 所有依赖已安装
echo.

REM 创建必要的目录
echo 📦 创建目录...
if not exist "uploads" mkdir uploads
if not exist "audio_output" mkdir audio_output
echo ✅ 目录已创建
echo.

echo ============================================
echo 🎉 启动 Web 应用...
echo ============================================
echo.
echo 💡 访问地址: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务
echo.

REM 启动 Flask
python app.py

pause
