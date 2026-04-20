@echo off
chcp 65001 > nul
echo ============================================
echo 🎙️  AI 语音助手 - 依赖安装脚本 (Windows)
echo ============================================
echo.

REM 检查 Python 版本
echo 📦 检查 Python 版本...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python 未安装或未添加到 PATH
    echo 请先安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查 pip
echo.
echo 📦 检查 pip...
pip --version
if %errorlevel% neq 0 (
    echo ❌ pip 未安装
    pause
    exit /b 1
)

REM 安装 Python 依赖
echo.
echo 📦 安装 Python 依赖...
echo 这可能需要几分钟，请稍候...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 测试导入
echo.
echo 📦 测试导入...
python -c "import speech_recognition; print('✅ SpeechRecognition')" 2>nul
python -c "import pyaudio; print('✅ PyAudio')" 2>nul
python -c "import requests; print('✅ Requests')" 2>nul
python -c "import edge_tts; print('✅ Edge-TTS')" 2>nul
python -c "import pyttsx3; print('✅ pyttsx3')" 2>nul
python -c "import numpy; print('✅ NumPy')" 2>nul

echo.
echo ============================================
echo ✅ 安装完成！
echo ============================================
echo.
echo 💡 下一步：
echo    1. 复制配置文件: copy .env.example .env
echo    2. 编辑 .env 文件，填入你的 API key
echo    3. 运行快速启动: python quick_start.py
echo.
pause
