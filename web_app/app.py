"""
AI 语音助手 Web 应用
Flask 后端服务器
"""

import os
import sys
import json
import tempfile
import uuid
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_voice_assistant.stt_engine import STTEngine
from ai_voice_assistant.ai_client import AIClient, create_ollama_client
from ai_voice_assistant.tts_engine import TTSEngine

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)

# 配置
UPLOAD_FOLDER = 'uploads'
AUDIO_OUTPUT_FOLDER = 'audio_output'
ALLOWED_EXTENSIONS = {'wav', 'webm', 'ogg', 'mp3', 'm4a'}

# 创建必要的目录
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 最大上传


# 全局实例（按需初始化）
stt_instances = {}
ai_instances = {}
tts_instance = None


def get_stt_instance(engine='sphinx', language='zh-CN'):
    """获取或创建 STT 实例"""
    key = f"{engine}_{language}"
    
    if key not in stt_instances:
        print(f"创建新的 STT 实例: {engine}")
        stt_instances[key] = STTEngine(
            engine=engine,
            language=language
        )
    
    return stt_instances[key]


def get_ai_instance(provider='openai', api_key='', model='gpt-3.5-turbo', 
                    api_base='', system_prompt=''):
    """获取或创建 AI 实例"""
    key = f"{provider}_{model}"
    
    if key not in ai_instances or ai_instances[key].api_key != api_key:
        print(f"创建新的 AI 实例: {provider} / {model}")
        
        if provider == 'ollama':
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
        else:  # openai 或其他兼容 OpenAI API 的服务
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


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============== API 路由 ==============

@app.route('/')
def index():
    """主页"""
    return send_file('templates/index.html')


@app.route('/api/stt', methods=['POST'])
def speech_to_text():
    """
    语音识别 API
    接收音频文件，返回识别的文字
    """
    try:
        # 检查是否有文件
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有上传音频文件'
            }), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '没有选择文件'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': '不支持的文件格式'
            }), 400
        
        # 获取参数
        engine = request.form.get('engine', 'sphinx')
        language = request.form.get('language', 'zh-CN')
        
        # 保存上传的文件
        filename = secure_filename(str(uuid.uuid4()) + '_' + file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"收到音频文件: {filename}, 大小: {os.path.getsize(filepath)} bytes")
        
        # 创建 STT 实例并识别
        stt = get_stt_instance(engine, language)
        
        # 使用 speech_recognition 识别文件
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        
        with sr.AudioFile(filepath) as source:
            # 调整噪音
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)
            
            # 识别
            print(f"正在识别音频...")
            if engine == 'whisper':
                # 使用 Whisper 识别
                import whisper
                import io
                
                # 转换音频格式
                audio_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
                audio_file = io.BytesIO(audio_data)
                
                # 加载模型
                model = whisper.load_model("base")
                result = model.transcribe(audio_file.read(), language=language.split('-')[0])
                text = result["text"].strip()
            else:
                # 使用 Sphinx 识别
                text = recognizer.recognize_sphinx(audio, language=language.split('-')[0])
        
        # 清理临时文件
        try:
            os.remove(filepath)
        except:
            pass
        
        print(f"识别成功: {text}")
        
        return jsonify({
            'success': True,
            'text': text,
            'engine': engine
        })
        
    except sr.UnknownValueError:
        return jsonify({
            'success': False,
            'error': '无法识别音频内容'
        }), 400
    except sr.RequestError as e:
        return jsonify({
            'success': False,
            'error': f'识别服务错误: {str(e)}'
        }), 500
    except Exception as e:
        print(f"STT 错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'处理失败: {str(e)}'
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    AI 对话 API
    接收用户消息，返回 AI 回复
    """
    try:
        data = request.get_json()
        
        message = data.get('message', '').strip()
        provider = data.get('provider', 'openai')
        model = data.get('model', 'gpt-3.5-turbo')
        api_key = data.get('api_key', '')
        system_prompt = data.get('system_prompt', '你是一个友好的AI助手。')
        
        if not message:
            return jsonify({
                'success': False,
                'error': '消息不能为空'
            }), 400
        
        if not api_key and provider != 'ollama':
            return jsonify({
                'success': False,
                'error': 'API Key 不能为空'
            }), 400
        
        print(f"收到对话请求: {message[:50]}... ({provider}/{model})")
        
        # 创建 AI 实例
        ai = get_ai_instance(provider, api_key, model, '', system_prompt)
        
        # 获取回复
        response = ai.chat(message)
        
        print(f"AI 回复: {response[:50]}...")
        
        return jsonify({
            'success': True,
            'response': response,
            'provider': provider,
            'model': model
        })
        
    except Exception as e:
        print(f"Chat 错误: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'对话失败: {str(e)}'
        }), 500


@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """
    语音合成 API
    接收文字，生成语音文件并返回 URL
    """
    try:
        data = request.get_json()
        
        text = data.get('text', '').strip()
        engine = data.get('engine', 'edge')
        voice = data.get('voice', 'zh-CN-XiaoxiaoNeural')
        
        if not text:
            return jsonify({
                'success': False,
                'error': '文字不能为空'
            }), 400
        
        print(f"收到 TTS 请求: {text[:50]}... ({engine})")
        
        # 创建 TTS 实例
        tts = get_tts_instance(engine, voice)
        
        # 生成音频文件
        timestamp = int(os.time() * 1000)
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
            'engine': engine
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
        'stt_instances': len(stt_instances),
        'ai_instances': len(ai_instances),
        'tts_initialized': tts_instance is not None
    })


@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """清理资源"""
    try:
        # 清理 STT 实例
        for key, stt in stt_instances.items():
            stt.cleanup()
        stt_instances.clear()
        
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


# 清理临时文件的函数
def cleanup_old_files():
    """清理超过1小时的临时文件"""
    import time
    
    now = time.time()
    max_age = 3600  # 1小时
    
    for folder in [UPLOAD_FOLDER, AUDIO_OUTPUT_FOLDER]:
        try:
            for filename in os.listdir(folder):
                filepath = os.path.join(folder, filename)
                if os.path.getmtime(filepath) < now - max_age:
                    os.remove(filepath)
                    print(f"删除旧文件: {filepath}")
        except Exception as e:
            print(f"清理文件时出错: {e}")


# 启动时清理旧文件
cleanup_old_files()


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 AI 语音助手 Web 应用启动中...")
    print("=" * 60)
    print("\n💡 访问地址: http://localhost:5000")
    print("\n📋 API 端点:")
    print("   - POST /api/stt    : 语音识别")
    print("   - POST /api/chat   : AI 对话")
    print("   - POST /api/tts    : 语音合成")
    print("   - GET  /api/health : 健康检查")
    print("   - POST /api/cleanup: 清理资源")
    print("\n⚙️  配置:")
    print(f"   上传目录: {UPLOAD_FOLDER}")
    print(f"   音频输出: {AUDIO_OUTPUT_FOLDER}")
    print("=" * 60)
    
    # 启动 Flask 应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
