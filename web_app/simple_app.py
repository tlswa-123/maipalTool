"""
AI 语音助手 Web 应用 (简化版)
使用浏览器原生 API 实现语音识别
"""

import os
import sys
import json
import time
import tempfile
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 只导入我们需要的模块
import ai_voice_assistant.ai_client as ai_client_module
import ai_voice_assistant.tts_engine as tts_engine_module

AIClient = ai_client_module.AIClient
create_ollama_client = ai_client_module.create_ollama_client
TTSEngine = tts_engine_module.TTSEngine

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)

# 配置
AUDIO_OUTPUT_FOLDER = 'audio_output'

# 创建必要的目录
os.makedirs(AUDIO_OUTPUT_FOLDER, exist_ok=True)

# 全局实例
ai_instances = {}
tts_instance = None

# CodeBuddy (腾讯云知识引擎) API 配置
# 注意: ck_ 开头的 Key 是 CodeBuddy Code 专属密钥
# 使用 /coding/v3 端点 (不是 /plan/v3)
CODEBUDDY_API_KEY = "ck_fjj7xzi09se8.Y-Yg84fogKg4ozeZZ9YFCq6dzHs5tBo8q4exJz2LE6M"
CODEBUDDY_API_URL = "https://api.lkeap.cloud.tencent.com/coding/v3"

# 老年男性声音选项
ELDERLY_MALE_VOICES = {
    'zh-CN-YunjianNeural': '中文-老年男声1',
    'zh-CN-YunxiNeural': '中文-老年男声2',
    'zh-CN-YunyangNeural': '中文-中年男声',
    'zh-TW-HsiaoChenNeural': '台湾-男声',
    'zh-HK-HiuMaanNeural': '香港-男声'
}
DEFAULT_ELDERLY_VOICE = 'zh-CN-YunjianNeural'  # 默认使用老年男声


class CodeBuddyClient:
    """CodeBuddy (腾讯云知识引擎) API 客户端 - 使用 CodeBuddy Agent SDK
    
    使用 CodeBuddy Agent SDK 调用 ck_ 开头的 API Key
    支持 iOA 环境: CODEBUDDY_INTERNET_ENVIRONMENT=ioa
    """
    
    def __init__(self, api_key, model='tc-code-latest', system_prompt='你是一个友好的AI助手。'):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.messages = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
        
        # 设置环境变量
        os.environ['CODEBUDDY_API_KEY'] = api_key
        os.environ['CODEBUDDY_INTERNET_ENVIRONMENT'] = 'ioa'
        
        # 导入 SDK
        try:
            from codebuddy_agent_sdk import query, CodeBuddyAgentOptions
            self.query = query
            self.CodeBuddyAgentOptions = CodeBuddyAgentOptions
            self.sdk_available = True
        except ImportError:
            print("⚠️ CodeBuddy Agent SDK 未安装，将使用模拟模式")
            self.sdk_available = False
        
    def chat(self, message):
        """发送消息并获取回复"""
        import asyncio
        
        # 添加用户消息
        self.messages.append({"role": "user", "content": message})
        
        if not self.sdk_available:
            # SDK 不可用，返回模拟回复
            return "[模拟模式] SDK 未安装，请运行: pip install codebuddy-agent-sdk"
        
        # 构建完整提示词（包含历史）
        full_prompt = self._build_prompt()
        
        # 使用 SDK 调用
        options = self.CodeBuddyAgentOptions(
            env={
                'CODEBUDDY_API_KEY': self.api_key,
                'CODEBUDDY_INTERNET_ENVIRONMENT': 'ioa'
            }
        )
        
        print(f"📤 使用 CodeBuddy SDK 发送请求...")
        print(f"📤 环境: iOA (tencent.sso.copilot.tencent.com)")
        
        # 运行异步查询
        response_text = asyncio.run(self._async_chat(full_prompt, options))
        
        # 添加助手消息到历史
        self.messages.append({"role": "assistant", "content": response_text})
        
        # 限制历史长度
        if len(self.messages) > 11:  # system + 10 条对话
            self.messages = [self.messages[0]] + self.messages[-10:]
        
        return response_text
    
    def _build_prompt(self):
        """构建包含历史消息的提示词"""
        prompt_parts = []
        for msg in self.messages:
            role = msg['role']
            content = msg['content']
            if role == 'system':
                prompt_parts.append(f"系统提示: {content}")
            elif role == 'user':
                prompt_parts.append(f"用户: {content}")
            elif role == 'assistant':
                prompt_parts.append(f"助手: {content}")
        return "\n\n".join(prompt_parts)
    
    async def _async_chat(self, prompt, options):
        """异步调用 SDK"""
        response_text = ""
        message_count = 0
        max_messages = 50  # 防止无限循环
        
        async for msg in self.query(prompt=prompt, options=options):
            message_count += 1
            if message_count > max_messages:
                break
                
            # 提取 AssistantMessage 中的文本内容
            if hasattr(msg, 'content') and msg.content:
                for block in msg.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                        print(f"📥 收到 AI 回复 ({len(response_text)} 字符)")
                        return response_text
            
            # ResultMessage 包含最终结果
            if hasattr(msg, 'result') and msg.result:
                response_text = msg.result
                print(f"📥 收到最终结果 ({len(response_text)} 字符)")
                return response_text
        
        return response_text if response_text else "抱歉，我没有收到有效的回复。"

def get_ai_instance(provider='codebuddy', api_key='', model='tc-code-latest',
                    api_base='', system_prompt=''):
    """获取或创建 AI 实例"""
    key = f"{provider}_{model}"

    if key not in ai_instances:
        print(f"创建新的 AI 实例: {provider} / {model}")

        if provider == 'codebuddy':
            # 使用 CodeBuddy (腾讯云知识引擎) API
            ai_instances[key] = CodeBuddyClient(
                api_key=CODEBUDDY_API_KEY,
                model=model,
                system_prompt=system_prompt
            )
        elif provider == 'ollama':
            ai_instances[key] = create_ollama_client(model)
        elif provider == 'zhipu':
            ai_instances[key] = AIClient(
                api_key=api_key,
                model=model,
                api_base_url='https://open.bigmodel.cn/api/paas/v4',
                system_prompt=system_prompt
            )
        elif provider == 'deepseek':
            ai_instances[key] = AIClient(
                api_key=api_key,
                model=model,
                api_base_url='https://api.deepseek.com/v1',
                system_prompt=system_prompt
            )
        else:  # openai
            api_base = api_base or 'https://api.openai.com/v1'
            ai_instances[key] = AIClient(
                api_key=api_key,
                model=model,
                api_base_url=api_base,
                system_prompt=system_prompt
            )

    return ai_instances[key]


def get_tts_instance(engine='edge', voice='zh-CN-XiaoxiaoNeural'):
    """获取或创建 TTS 实例"""
    global tts_instance

    if tts_instance is None:
        print(f"创建新的 TTS 实例: {engine}")
        tts_instance = TTSEngine(
            engine=engine,
            voice=voice
        )

    return tts_instance


# ============== API 路由 ==============

@app.route('/')
def index():
    """主页"""
    return send_file('templates/simple_index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    AI 对话 API - 使用 CodeBuddy (腾讯云知识引擎)
    """
    try:
        data = request.get_json()

        message = data.get('message', '').strip()
        # 使用 CodeBuddy
        provider = 'codebuddy'
        model = data.get('model', 'tc-code-latest')  # 默认使用 Auto 智能路由
        system_prompt = data.get('system_prompt', '你是一个友好的AI助手。')

        print(f"\n{'='*60}")
        print(f"收到对话请求:")
        print(f"  消息: {message[:100]}...")
        print(f"  提供商: CodeBuddy (腾讯云知识引擎)")
        print(f"  模型: {model}")
        print(f"  API Key: {CODEBUDDY_API_KEY[:20]}...")
        print(f"  API URL: {CODEBUDDY_API_URL}")
        print(f"  系统提示: {system_prompt[:50]}...")
        print(f"{'='*60}\n")

        if not message:
            return jsonify({
                'success': False,
                'error': '消息不能为空'
            }), 400

        # 创建 AI 实例 - 使用 CodeBuddy
        print(f"🤖 创建 AI 实例 (CodeBuddy)...")
        ai = get_ai_instance(provider, CODEBUDDY_API_KEY, model, '', system_prompt)

        # 获取回复
        print(f"🤖 发送消息给 AI...")
        response = ai.chat(message)

        print(f"\n✅ AI 回复成功:")
        print(f"  回复: {response[:100]}...")
        print(f"  长度: {len(response)} 字符")
        print(f"{'='*60}\n")

        return jsonify({
            'success': True,
            'response': response,
            'provider': 'CodeBuddy',
            'model': model
        })

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ Chat 错误:")
        print(f"  错误类型: {type(e).__name__}")
        print(f"  错误信息: {e}")
        print(f"{'='*60}\n")
        
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f'对话失败: {str(e)}'
        }), 500


@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """
    语音合成 API - 默认使用老年男性声音
    """
    try:
        data = request.get_json()

        text = data.get('text', '').strip()
        engine = data.get('engine', 'edge')
        # 默认使用老年男性声音
        voice = data.get('voice', 'zh-CN-YunjianNeural')

        if not text:
            return jsonify({
                'success': False,
                'error': '文字不能为空'
            }), 400

        print(f"收到 TTS 请求: {text[:50]}... ({engine}, {voice})")

        # 创建 TTS 实例 - 强制使用老年男性声音作为默认
        tts = get_tts_instance(engine, voice)

        # 生成音频文件
        timestamp = int(time.time() * 1000)
        filename = f"tts_{timestamp}.mp3"
        filepath = os.path.join(AUDIO_OUTPUT_FOLDER, filename)

        # 保存为文件
        if engine == 'edge':
            tts.save_to_file(text, filepath)
        else:
            # pyttsx3 不支持保存，使用 edge 作为备选
            tts.save_to_file(text, filepath)

        print(f"TTS 完成: {filename}")

        # 返回文件 URL
        audio_url = f"/audio/{filename}"

        return jsonify({
            'success': True,
            'audio_url': audio_url,
            'engine': engine,
            'voice': voice
        })

    except Exception as e:
        print(f"TTS 错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'语音合成失败: {str(e)}'
        }), 500


@app.route('/audio/<filename>')
def serve_audio(filename):
    """提供音频文件"""
    return send_file(
        os.path.join(AUDIO_OUTPUT_FOLDER, filename),
        mimetype='audio/mpeg'
    )


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'ai_instances': len(ai_instances),
        'tts_initialized': tts_instance is not None
    })


@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """清理资源"""
    try:
        # 清理 AI 实例
        ai_instances.clear()

        # 清理 TTS 实例
        global tts_instance
        if tts_instance:
            tts_instance.cleanup()
            tts_instance = None

        return jsonify({
            'success': True,
            'message': '资源已清理'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AI 语音助手 Web 应用启动中...")
    print("=" * 60)
    print("\n💡 访问地址: http://localhost:5000")
    print("\n📋 功能:")
    print("   - ✅ 使用浏览器原生 API 进行语音识别")
    print("   - ✅ AI 对话 (支持多种服务)")
    print("   - ✅ 语音合成")
    print("\n⚙️  配置:")
    print(f"   音频输出: {AUDIO_OUTPUT_FOLDER}")
    print("=" * 60)

    # 启动 Flask 应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
