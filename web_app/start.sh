#!/bin/bash

echo "============================================"
echo "🚀 AI 语音助手 Web 应用启动脚本"
echo "============================================"
echo ""

# 检查 Python
echo "📦 检查 Python..."
python3 --version

# 检查依赖
echo ""
echo "📦 检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask 未安装"
    echo "💡 请运行: pip install -r requirements.txt"
    exit 1
fi

echo "✅ 所有依赖已安装"
echo ""

# 创建必要的目录
echo "📦 创建目录..."
mkdir -p uploads
mkdir -p audio_output
echo "✅ 目录已创建"
echo ""

# 启动应用
echo "============================================"
echo "🎉 启动 Web 应用..."
echo "============================================"
echo ""
echo "💡 访问地址: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动 Flask
python3 app.py
