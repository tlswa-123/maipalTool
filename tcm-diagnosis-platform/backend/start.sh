#!/bin/bash

# 中医智能诊断平台 - 后端启动脚本

echo "🚀 中医智能诊断平台 - 后端启动"
echo "=================================="

# 检查Python版本
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 启动服务器
echo "✅ 启动后端服务..."
echo "📍 API地址: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python app.py
