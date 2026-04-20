"""
AI 对话客户端
支持多种 AI 服务提供商
"""

import requests
import json
from typing import Optional, List, Dict, Callable


class AIClient:
    """AI 对话客户端"""
    
    def __init__(self,
                 api_key: str,
                 model: str = 'gpt-3.5-turbo',
                 api_base_url: str = 'https://api.openai.com/v1',
                 system_prompt: str = '你是一个友好的AI助手。',
                 max_tokens: int = 500,
                 temperature: float = 0.7):
        """
        初始化 AI 客户端
        
        Args:
            api_key: API 密钥
            model: 模型名称
            api_base_url: API 基础 URL
            system_prompt: 系统提示词
            max_tokens: 最大生成长度
            temperature: 温度参数（控制创造性）
        """
        self.api_key = api_key
        self.model = model
        self.api_base_url = api_base_url.rstrip('/')
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # 对话历史
        self.messages: List[Dict[str, str]] = []
        self.max_history = 10
        
        # 添加系统消息
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # 回调函数（用于流式输出）
        self.on_message: Optional[Callable] = None
        self.on_complete: Optional[Callable] = None
        
        print(f"✅ AI 客户端初始化完成")
        print(f"   模型: {model}")
        print(f"   API: {api_base_url}")
    
    def chat(self, message: str, stream: bool = False) -> str:
        """
        发送消息并获取回复
        
        Args:
            message: 用户消息
            stream: 是否使用流式输出
        
        Returns:
            AI 的回复
        """
        if not message.strip():
            return ""
        
        # 添加用户消息
        self.messages.append({
            "role": "user",
            "content": message
        })
        
        # 截断历史消息
        if len(self.messages) > self.max_history:
            self.messages = [self.messages[0]] + self.messages[-(self.max_history-1):]
        
        try:
            print("🤖 AI 正在思考...")
            
            if stream and self.on_message:
                return self._chat_stream()
            else:
                return self._chat_once()
                
        except Exception as e:
            print(f"❌ AI 响应错误: {e}")
            # 返回错误消息
            error_msg = f"抱歉，我遇到了一些问题: {str(e)}"
            return error_msg
    
    def _chat_once(self) -> str:
        """一次性获取完整回复"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        url = f"{self.api_base_url}/chat/completions"
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        assistant_message = result['choices'][0]['message']['content']
        
        # 添加助手消息到历史
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def _chat_stream(self) -> str:
        """流式获取回复"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": True
        }
        
        url = f"{self.api_base_url}/chat/completions"
        
        full_response = ""
        
        try:
            response = requests.post(url, headers=headers, json=data, stream=True, timeout=30)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        
                        try:
                            chunk = json.loads(data_str)
                            delta = chunk.get('choices', [{}])[0].get('delta', {})
                            content = delta.get('content', '')
                            
                            if content:
                                full_response += content
                                if self.on_message:
                                    self.on_message(content)
                        
                        except json.JSONDecodeError:
                            continue
            
            # 添加完整回复到历史
            self.messages.append({
                "role": "assistant",
                "content": full_response
            })
            
            if self.on_complete:
                self.on_complete(full_response)
            
            return full_response
            
        except Exception as e:
            print(f"流式输出错误: {e}")
            return full_response
    
    def clear_history(self):
        """清空对话历史（保留系统提示）"""
        system_messages = [msg for msg in self.messages if msg['role'] == 'system']
        self.messages = system_messages
        print("🧹 对话历史已清空")
    
    def set_system_prompt(self, prompt: str):
        """设置系统提示词"""
        # 移除旧的系统消息
        self.messages = [msg for msg in self.messages if msg['role'] != 'system']
        # 添加新的系统消息
        self.messages.insert(0, {
            "role": "system",
            "content": prompt
        })
        self.system_prompt = prompt
        print(f"✅ 系统提示词已更新")
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.messages.copy()
    
    def set_on_message_callback(self, callback: Callable):
        """设置流式输出回调函数"""
        self.on_message = callback
    
    def set_on_complete_callback(self, callback: Callable):
        """设置完成回调函数"""
        self.on_complete = callback


# 快捷工厂函数
def create_openai_client(api_key: str, model: str = 'gpt-3.5-turbo') -> AIClient:
    """创建 OpenAI 客户端"""
    return AIClient(
        api_key=api_key,
        model=model,
        api_base_url='https://api.openai.com/v1',
        system_prompt='你是一个友好、乐于助人的AI助手。'
    )


def create_zhipu_client(api_key: str, model: str = 'glm-4') -> AIClient:
    """创建智谱 AI 客户端"""
    return AIClient(
        api_key=api_key,
        model=model,
        api_base_url='https://open.bigmodel.cn/api/paas/v4',
        system_prompt='你是一个友好、乐于助人的AI助手。'
    )


def create_deepseek_client(api_key: str, model: str = 'deepseek-chat') -> AIClient:
    """创建 DeepSeek 客户端"""
    return AIClient(
        api_key=api_key,
        model=model,
        api_base_url='https://api.deepseek.com/v1',
        system_prompt='你是一个友好、乐于助人的AI助手。'
    )


def create_ollama_client(model: str = 'llama2') -> AIClient:
    """创建 Ollama 客户端（本地部署）"""
    return AIClient(
        api_key='ollama',  # Ollama 不需要 API key
        model=model,
        api_base_url='http://localhost:11434/v1',
        system_prompt='你是一个友好、乐于助人的AI助手。'
    )


# 简单的测试函数
def test_ai():
    """测试 AI 对话"""
    print("=" * 50)
    print("🤖 AI 对话测试")
    print("=" * 50)
    
    # 示例：使用本地 Ollama（不需要 API key）
    # 如果你没有安装 Ollama，可以使用其他服务
    
    # 方式1: 使用 Ollama（需要先安装并启动 Ollama）
    try:
        client = create_ollama_client(model='llama2')
        print("使用本地 Ollama 模型")
    except:
        print("⚠️  未检测到 Ollama，请使用其他 AI 服务")
        print("   示例: client = create_openai_client(api_key='your-key')")
        return
    
    # 方式2: 使用 OpenAI（需要 API key）
    # client = create_openai_client(api_key='your-api-key')
    
    # 方式3: 使用智谱 AI（需要 API key）
    # client = create_zhipu_client(api_key='your-api-key')
    
    try:
        # 设置流式输出回调
        def on_chunk(chunk: str):
            print(chunk, end='', flush=True)
        
        def on_complete(full: str):
            print(f"\n\n✅ 完成回复，共 {len(full)} 字符")
        
        client.set_on_message_callback(on_chunk)
        client.set_on_complete_callback(on_complete)
        
        # 发送消息
        while True:
            print("\n" + "=" * 50)
            user_input = input("你 (输入 'quit' 退出): ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                break
            
            if not user_input:
                continue
            
            print("\nAI 回复: ", end='', flush=True)
            response = client.chat(user_input, stream=True)
            
    except KeyboardInterrupt:
        print("\n⚠️  用户中断")


if __name__ == "__main__":
    test_ai()
