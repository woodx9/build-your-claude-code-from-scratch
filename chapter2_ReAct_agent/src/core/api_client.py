from openai import OpenAI
from typing import Dict, Any, Optional


class APIClient:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        单例模式初始化API客户端
        """
        if not self._initialized:
            self.api_key = "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"
            self.base_url = "https://openrouter.ai/api/v1"
            self.model = "anthropic/claude-sonnet-4"
            
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            self._initialized = True
    
    def get_completion(self, request_params: Dict[str, Any]):
        """
        发送聊天完成请求并返回消息
        
        Args:
            request_params: 请求参数字典，包含model, messages等
            
        Returns:
            返回AI助手的回复消息对象
        """

        request_params["model"] = self.model
        try:
            response = self.client.chat.completions.create(**request_params)
            return response.choices[0].message
        except Exception as e:
            raise Exception(f"API请求失败: {str(e)}")