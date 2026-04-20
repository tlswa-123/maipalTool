#!/usr/bin/env python3
"""
诊断工具 - 帮助诊断 OpenAI API 问题
"""

import requests
import json
import sys

API_URL = "http://localhost:5000"

def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_health():
    """测试健康检查"""
    print_section("1️⃣  测试健康检查")

    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        print(f"✅ 状态码: {response.status_code}")
        print(f"📊 响应:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return True
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_openai_api_key(api_key):
    """测试 OpenAI API Key"""
    print_section("2️⃣  测试 OpenAI API Key")

    url = "https://api.openai.com/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"📤 请求 OpenAI API...")
    print(f"   API Key: {api_key[:10]}...{api_key[-4:]}")

    try:
        response = requests.get(url, headers=headers, timeout=10)

        print(f"\n📥 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Key 有效！")
            print(f"\n📊 可用模型（前10个）:")
            for model in result['data'][:10]:
                print(f"   - {model['id']}")
            return True
        else:
            print(f"❌ API Key 无效")
            print(f"\n📥 错误响应:")
            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except:
                print(response.text)
            return False

    except requests.exceptions.Timeout:
        print(f"⏱️  请求超时")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_api(api_key):
    """测试聊天 API"""
    print_section("3️⃣  测试聊天 API")

    data = {
        "message": "你好",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key": api_key,
        "system_prompt": "你是一个友好的AI助手。"
    }

    print(f"📤 发送聊天请求...")
    print(f"   消息: {data['message']}")
    print(f"   提供商: {data['provider']}")
    print(f"   模型: {data['model']}")

    try:
        response = requests.post(f"{API_URL}/api/chat", json=data, timeout=30)

        print(f"\n📥 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ 聊天 API 成功！")
            print(f"\n📊 响应内容:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            if result.get('success'):
                print(f"\n🤖 AI 回复:")
                print(f"   {result.get('response', '无回复')}")
                return True
            else:
                print(f"\n❌ AI 回复失败:")
                print(f"   错误: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 聊天 API 请求失败")
            print(f"\n📥 错误响应:")
            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except:
                print(response.text)
            return False

    except requests.exceptions.Timeout:
        print(f"⏱️  请求超时（30秒）")
        print(f"💡 建议：检查网络连接或使用其他 AI 服务")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tts_api():
    """测试语音合成 API"""
    print_section("4️⃣  测试语音合成 API")

    data = {
        "text": "你好，这是一个测试。",
        "engine": "edge",
        "voice": "zh-CN-XiaoxiaoNeural"
    }

    print(f"📤 发送 TTS 请求...")
    print(f"   文字: {data['text'][:30]}...")

    try:
        response = requests.post(f"{API_URL}/api/tts", json=data, timeout=30)

        print(f"\n📥 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ TTS API 成功！")
            print(f"\n📊 响应内容:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ TTS API 请求失败")
            print(f"\n📥 错误响应:")
            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except:
                print(response.text)
            return False

    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🔍 AI 语音助手诊断工具")
    print("=" * 60)

    # 获取 API Key
    print("\n请输入你的 OpenAI API Key:")
    print("(也可以留空跳过 API Key 测试)")
    api_key = input("> ").strip()

    # 运行测试
    results = []

    # 测试 1: 健康检查
    results.append(("健康检查", test_health()))

    # 测试 2: OpenAI API Key
    if api_key:
        results.append(("OpenAI API Key", test_openai_api_key(api_key)))
    else:
        print_section("2️⃣  测试 OpenAI API Key")
        print("⏭️  跳过（未提供 API Key）")

    # 测试 3: 聊天 API
    if api_key:
        results.append(("聊天 API", test_chat_api(api_key)))
    else:
        print_section("3️⃣  测试聊天 API")
        print("⏭️  跳过（未提供 API Key）")

    # 测试 4: TTS API
    results.append(("语音合成 API", test_tts_api()))

    # 打印总结
    print_section("📋 诊断总结")

    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {name}: {status}")

    # 给出建议
    print_section("💡 建议")

    all_passed = all(success for _, success in results)

    if all_passed:
        print("✅ 所有测试都通过了！")
        print("🎉 你的系统配置完全正常，可以在浏览器中使用 AI 语音助手了！")
        print("\n📖 使用指南:")
        print("   1. 访问 http://localhost:5000")
        print("   2. 在设置中填入你的 API Key")
        print("   3. 选择模型（推荐 gpt-3.5-turbo）")
        print("   4. 开始对话！")
    else:
        print("❌ 部分测试失败，请检查以下内容:\n")

        for name, success in results:
            if not success:
                if name == "健康检查":
                    print(f"   • {name} 失败:")
                    print("     - 检查服务器是否运行: ps aux | grep simple_app.py")
                    print("     - 重启服务器: cd web_app && python3 simple_app.py")

                elif name == "OpenAI API Key":
                    print(f"   • {name} 失败:")
                    print("     - 检查 API Key 是否正确")
                    print("     - 检查账户余额是否充足")
                    print("     - 访问 https://platform.openai.com/api-keys 重新获取")
                    print("     - 考虑使用智谱 AI 或 DeepSeek（有免费额度）")

                elif name == "聊天 API":
                    print(f"   • {name} 失败:")
                    print("     - 检查 API Key 是否有效")
                    print("     - 检查网络连接")
                    print("     - 查看服务器日志: tail -f web_app/app.log")
                    print("     - 考虑使用其他 AI 服务")

                elif name == "语音合成 API":
                    print(f"   • {name} 失败:")
                    print("     - 检查依赖是否安装: pip3 list | grep edge-tts")
                    print("     - 查看服务器日志: tail -f web_app/app.log")

    print("\n" + "=" * 60)
    print("🔍 诊断完成")
    print("=" * 60 + "\n")

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
