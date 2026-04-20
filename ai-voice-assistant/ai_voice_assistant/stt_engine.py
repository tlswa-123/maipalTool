"""
语音识别引擎 (Speech-to-Text)
支持多种识别引擎，可灵活切换
"""

import pyaudio
import speech_recognition as sr
import numpy as np
import time
from typing import Optional, Callable
from threading import Thread, Event


class STTEngine:
    """语音识别引擎"""
    
    def __init__(self, 
                 engine: str = 'sphinx',
                 language: str = 'zh-CN',
                 chunk_size: int = 1024,
                 sample_rate: int = 16000,
                 silence_threshold: int = 500,
                 silence_duration: float = 1.0):
        """
        初始化语音识别引擎
        
        Args:
            engine: 识别引擎 ('sphinx' 或 'whisper')
            language: 识别语言 ('zh-CN', 'en-US' 等)
            chunk_size: 音频块大小
            sample_rate: 采样率
            silence_threshold: 静音检测阈值
            silence_duration: 静音持续多久自动停止录音
        """
        self.engine = engine
        self.language = language
        self.chunk_size = chunk_size
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        
        # 初始化识别器
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = silence_threshold
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.operation_timeout = None
        
        # PyAudio 实例
        self.pyaudio = pyaudio.PyAudio()
        
        # 控制标志
        self.is_recording = False
        self.stop_event = Event()
        
        print(f"✅ STT 引擎初始化完成")
        print(f"   引擎: {engine}")
        print(f"   语言: {language}")
    
    def _get_audio_stream(self):
        """创建音频流"""
        return self.pyaudio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
    
    def listen_once(self, timeout: Optional[int] = None) -> Optional[str]:
        """
        监听一次（按 Enter 或超时停止）
        
        Args:
            timeout: 超时时间（秒），None 表示不超时
        
        Returns:
            识别的文字，失败返回 None
        """
        try:
            with sr.Microphone(sample_rate=self.sample_rate) as source:
                print("\n🎤 正在录音... 按 Enter 停止")
                
                # 自动噪音校准
                print("🔇 正在降噪校准...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("🔊 可以开始说话了")
                
                # 监听
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=None)
                
                print("🔍 正在识别...")
                text = self._recognize_audio(audio)
                
                if text:
                    print(f"✅ 识别成功: \"{text}\"")
                else:
                    print("❌ 识别失败")
                
                return text
                
        except sr.WaitTimeoutError:
            print("⏰ 录音超时")
            return None
        except sr.RequestError as e:
            print(f"❌ 请求错误: {e}")
            return None
        except sr.UnknownValueError:
            print("❌ 无法识别音频")
            return None
        except Exception as e:
            print(f"❌ 录音错误: {e}")
            return None
    
    def _recognize_audio(self, audio) -> Optional[str]:
        """识别音频"""
        try:
            if self.engine == 'whisper':
                # 使用 Whisper 识别（需要安装 whisper）
                import whisper
                import io
                
                # 将 audio 转换为格式
                audio_data = audio.get_raw_data(
                    convert_rate=16000,
                    convert_width=2
                )
                audio_file = io.BytesIO(audio_data)
                
                # 加载模型
                model = whisper.load_model("base")
                result = model.transcribe(audio_file.read(), language=self.language.split('-')[0])
                
                return result["text"].strip()
            
            else:  # sphinx (默认，离线)
                return self.recognizer.recognize_sphinx(audio, language=self.language.split('-')[0])
                
        except ImportError:
            if self.engine == 'whisper':
                print("⚠️  Whisper 未安装，回退到 sphinx")
                self.engine = 'sphinx'
                return self._recognize_audio(audio)
            else:
                print("⚠️  请安装语音识别库:")
                print("   - Sphinx (离线): pip install SpeechRecognition")
                print("   - Whisper (在线): pip install openai-whisper")
                return None
        except Exception as e:
            print(f"识别错误: {e}")
            return None
    
    def listen_with_silence_detection(self, 
                                      min_duration: float = 1.0,
                                      on_speech_detected: Optional[Callable] = None) -> Optional[str]:
        """
        使用静音检测自动录音
        
        Args:
            min_duration: 最短录音时长（秒）
            on_speech_detected: 检测到语音时的回调函数
        
        Returns:
            识别的文字
        """
        print("\n🎤 正在录音... (检测到语音后自动停止)")
        
        stream = self._get_audio_stream()
        frames = []
        
        try:
            silence_counter = 0
            start_time = time.time()
            has_speech = False
            
            while not self.stop_event.is_set():
                data = stream.read(self.chunk_size)
                frames.append(data)
                
                # 计算音量
                audio_data = np.frombuffer(data, dtype=np.int16)
                volume = np.abs(audio_data).mean()
                
                # 静音检测
                if volume > self.silence_threshold:
                    has_speech = True
                    silence_counter = 0
                    
                    if on_speech_detected:
                        on_speech_detected(volume)
                else:
                    silence_counter += self.chunk_size / self.sample_rate
                    
                    # 如果有语音且静音超过阈值时间，且满足最短时长
                    if has_speech and silence_counter > self.silence_duration:
                        if time.time() - start_time >= min_duration:
                            break
                
                # 显示音量条
                bar_length = int(volume / 20)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                print(f"\r🔊 {bar} {volume:.1f}", end="", flush=True)
            
            print()  # 换行
            
            # 转换音频格式
            audio_data = b''.join(frames)
            audio_source = sr.AudioData(
                audio_data,
                sample_rate=self.sample_rate,
                sample_width=2
            )
            
            # 识别
            print("🔍 正在识别...")
            text = self._recognize_audio(audio_source)
            
            if text:
                print(f"✅ 识别成功: \"{text}\"")
            else:
                print("❌ 识别失败")
            
            return text
            
        except Exception as e:
            print(f"\n❌ 录音错误: {e}")
            return None
        finally:
            stream.stop_stream()
            stream.close()
    
    def stop_recording(self):
        """停止录音（用于异步录音）"""
        self.stop_event.set()
    
    def reset_stop_event(self):
        """重置停止事件"""
        self.stop_event.clear()
    
    def cleanup(self):
        """清理资源"""
        if hasattr(self, 'pyaudio'):
            self.pyaudio.terminate()
        print("🧹 STT 资源已清理")


# 简单的测试函数
def test_stt():
    """测试语音识别"""
    print("=" * 50)
    print("🎤 语音识别测试")
    print("=" * 50)
    
    # 创建引擎
    stt = STTEngine(
        engine='sphinx',  # 使用离线引擎，不需要 API
        language='zh-CN'
    )
    
    try:
        # 方式1: 按 Enter 停止
        text = stt.listen_once()
        
        if text:
            print(f"\n识别结果: {text}")
        else:
            print("\n未识别到语音")
    
    except KeyboardInterrupt:
        print("\n⚠️  用户中断")
    
    finally:
        stt.cleanup()


if __name__ == "__main__":
    test_stt()
