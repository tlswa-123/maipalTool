#!/usr/bin/env python3
"""
测试 AI 对话 API
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_health():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    response = requests.get(f"{API_URL}/api/health")
    print(f"✅ 健康检查: {response.json()}")

def test_chat_with_ollama():
    """测试 Ollama 对话"""
    print("\n🔍 测试 Ollama 对话...")
    
    data = {
        "message": "你好",
        "provider": "ollama",
        "model": "llama2",
        "system_prompt": "你是一个友好的AI助手。"
    }
    
    response = requests.post(f"{API_URL}/api/chat", json=data)
    print(f"✅ Ollama 响应: {response.json()}")

def test_chat_with_zhipu():
    """测试智谱 AI 对话"""
    print("\n🔍 测试智谱 AI 对话...")
    
    # 替换为你的 API Key
    api_key = "your-zhipu-api-key"
    
    data = {
        "message": "你好",
        "provider": "zhipu",
        "model": "glm-4",
        "api_key": api_key,
        "system_prompt": "你是一个友好的AI助手。"
    }
    
    response = requests.post(f"{API_URL}/api/chat", json=data)
    print(f"✅ 智谱 AI 响应: {response.json()}")

def test_tts():
    """测试语音合成"""
    print("\n🔍 测试语音合成...")
    
    data = {
        "text": "你好，这是一个测试。",
        "engine": "edge",
        "voice": "zh-CN-XiaoxiaoNeural"
    }
    
    response = requests.post(f"{API_URL}/api/tts", json=data)
    print(f"✅ TTS 响应: {response.json()}")
    
    if response.json().get('success'):
        audio_url = f"{API_URL}{response.json()['audio_url']}"
        print(f"🔊 音频 URL: {audio_url}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 API 测试")
    print("=" * 60)
    
    try:
        # 测试健康检查
        test_health()
        
        # 测试 Ollama（需要先安装 Ollama）
        # test_chat_with_ollama()
        
        # 测试智谱 AI（需要 API Key）
        # test_chat_with_zhipu()
        
        # 测试 TTS
        test_tts()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
