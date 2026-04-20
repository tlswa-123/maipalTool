#!/usr/bin/env python3
"""
简单的 OpenAI API 测试
直接测试 OpenAI API，不通过 Web 应用
"""

import requests
import json

# 在这里填入你的 API Key
API_KEY = "sk-your-api-key-here"

def test_openai_direct():
    """直接测试 OpenAI API"""
    print("=" * 60)
    print("🔍 直接测试 OpenAI API")
    print("=" * 60)

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "你是一个友好的AI助手。"},
            {"role": "user", "content": "你好，请简单回答"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }

    print(f"\n📤 发送请求...")
    print(f"   URL: {url}")
    print(f"   模型: {data['model']}")
    print(f"   消息: {data['messages'][1]['content']}")
    print(f"   API Key: {API_KEY[:10]}...{API_KEY[-4:]}")

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        print(f"\n📥 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"\n✅ 测试成功！")
            print(f"\n🤖 AI 回复:")
            print(f"   {message}")
            print(f"\n📊 使用 token:")
            print(f"   提示: {result['usage']['prompt_tokens']}")
            print(f"   完成: {result['usage']['completion_tokens']}")
            print(f"   总计: {result['usage']['total_tokens']}")
            return True
        else:
            print(f"\n❌ 测试失败")
            print(f"\n📥 响应内容:")
            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except:
                print(response.text)
            return False

    except requests.exceptions.Timeout:
        print(f"\n⏱️  请求超时")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 请修改这里的 API Key
    if API_KEY == "sk-your-api-key-here":
        print("⚠️  请先修改脚本中的 API_KEY 变量")
        print("   将 'sk-your-api-key-here' 替换为你的真实 API Key")
        exit(1)

    success = test_openai_direct()

    print("\n" + "=" * 60)
    if success:
        print("✅ API Key 测试通过！可以正常使用。")
    else:
        print("❌ API Key 测试失败，请检查：")
        print("   1. API Key 是否正确")
        print("   2. 账户是否有余额")
        print("   3. API Key 是否已激活")
        print("   4. 网络连接是否正常")
    print("=" * 60)

    exit(0 if success else 1)
