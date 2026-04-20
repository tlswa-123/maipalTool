#!/bin/bash

echo "============================================"
echo "🎙️  AI 语音助手 - 依赖安装脚本"
echo "============================================"
echo ""

# 检查 Python 版本
echo "📦 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python 版本: $python_version"

# 检查 pip
echo ""
echo "📦 检查 pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 已安装"
else
    echo "❌ pip3 未安装，请先安装 pip"
    exit 1
fi

# 安装 Python 依赖
echo ""
echo "📦 安装 Python 依赖..."
echo "这可能需要几分钟，请稍候..."
pip3 install -r requirements.txt

# 检查操作系统
echo ""
echo "📦 检查操作系统..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 检测到 macOS"
    
    # 检查是否安装了 Homebrew
    if command -v brew &> /dev/null; then
        echo "✅ Homebrew 已安装"
        
        # 安装 PortAudio
        echo ""
        echo "📦 安装 PortAudio..."
        brew install portaudio
        
    else
        echo "⚠️  未安装 Homebrew"
        echo "   PyAudio 可能需要手动安装"
    fi
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 检测到 Linux"
    
    # 检查是否是 Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        echo "✅ apt-get 已安装"
        
        # 安装 PortAudio
        echo ""
        echo "📦 安装 PortAudio..."
        sudo apt-get update
        sudo apt-get install -y portaudio19-dev
        
    elif command -v yum &> /dev/null; then
        echo "✅ yum 已安装"
        
        # 安装 PortAudio
        echo ""
        echo "📦 安装 PortAudio..."
        sudo yum install -y portaudio-devel
        
    else
        echo "⚠️  未知的 Linux 发行版"
        echo "   PyAudio 可能需要手动安装"
    fi
    
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "🪟 检测到 Windows"
    echo "✅ Windows 不需要额外安装 PortAudio"
    
else
    echo "⚠️  未知的操作系统"
fi

# 测试导入
echo ""
echo "📦 测试导入..."
python3 -c "
try:
    import speech_recognition
    print('✅ SpeechRecognition')
except ImportError:
    print('❌ SpeechRecognition')

try:
    import pyaudio
    print('✅ PyAudio')
except ImportError:
    print('❌ PyAudio')

try:
    import requests
    print('✅ Requests')
except ImportError:
    print('❌ Requests')

try:
    import edge_tts
    print('✅ Edge-TTS')
except ImportError:
    print('❌ Edge-TTS')

try:
    import pyttsx3
    print('✅ pyttsx3')
except ImportError:
    print('❌ pyttsx3')

try:
    import numpy
    print('✅ NumPy')
except ImportError:
    print('❌ NumPy')
"

echo ""
echo "============================================"
echo "✅ 安装完成！"
echo "============================================"
echo ""
echo "💡 下一步："
echo "   1. 复制配置文件: cp .env.example .env"
echo "   2. 编辑 .env 文件，填入你的 API key"
echo "   3. 运行快速启动: python quick_start.py"
echo ""
