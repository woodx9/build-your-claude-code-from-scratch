import os
from openai import OpenAI
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class APIClient:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        单例模式初始化API客户端，使用环境变量配置
        """
        if not self._initialized:
            # 加载.env文件
            load_dotenv()
            
            # 从环境变量获取配置，如果不存在则抛出错误
            self.api_key = self._get_required_env_var("OPENAI_API_KEY")
            self.base_url = self._get_required_env_var("OPENAI_BASE_URL") 
            self.model = self._get_required_env_var("OPENAI_MODEL")
            
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            self._initialized = True
    
    def _get_required_env_var(self, var_name: str) -> str:
        """
        获取必需的环境变量，如果不存在则抛出错误
        
        Args:
            var_name: 环境变量名称
            
        Returns:
            环境变量的值
            
        Raises:
            ValueError: 当环境变量不存在或为空时
        """
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"环境变量 {var_name} 未设置或为空。请检查 .env 文件中的配置。")
        return value
    
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
