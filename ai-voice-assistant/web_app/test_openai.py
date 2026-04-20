#!/usr/bin/env python3
"""
测试 OpenAI API
"""

import requests
import json
import sys

# 从命令行参数获取 API Key
if len(sys.argv) > 1:
    API_KEY = sys.argv[1]
else:
    API_KEY = input("请输入你的 OpenAI API Key: ")

API_URL = "http://localhost:5000"

def test_openai():
    """测试 OpenAI 对话"""
    print("=" * 60)
    print("🔍 测试 OpenAI API")
    print("=" * 60)
    
    data = {
        "message": "你好，请简单回答",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": API_KEY,
        "system_prompt": "你是一个友好的AI助手。"
    }
    
    print(f"\n📤 发送请求到 OpenAI...")
    print(f"   消息: {data['message']}")
    print(f"   模型: {data['model']}")
    print(f"   API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    
    try:
        response = requests.post(f"{API_URL}/api/chat", json=data, timeout=30)
        
        print(f"\n📥 响应状态码: {response.status_code}")
        print(f"📥 响应头: {dict(response.headers)}")
        
        try:
            result = response.json()
            print(f"\n📥 响应内容:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except:
            print(f"\n📥 原始响应:")
            print(response.text)
        
        if response.status_code == 200 and result.get('success'):
            print("\n✅ OpenAI API 测试成功！")
            return True
        else:
            print(f"\n❌ OpenAI API 测试失败")
            return False
            
    except requests.exceptions.Timeout:
        print("\n⏱️ 请求超时")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_openai()
    sys.exit(0 if success else 1)
