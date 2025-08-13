from openai import OpenAI
from typing import Dict, Any, Optional, Generator, Tuple
import json
import os
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageFunctionToolCall
from openai.types.chat.chat_completion_message_function_tool_call import Function


# 加载环境变量
load_dotenv()


class APIClient:
    _instance = None
    _initialized = False
    _total_cost = 0
    
    @property
    def total_cost(self):
        return round(self._total_cost, 2)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        单例模式初始化API客户端
        """
        if not self._initialized:
            # 从环境变量读取配置
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.base_url = os.getenv("OPENAI_BASE_URL")
            self.model = os.getenv("OPENAI_MODEL")
            
            # 检查必要的环境变量是否存在
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY 环境变量未设置")
            if not self.base_url:
                raise ValueError("OPENAI_BASE_URL 环境变量未设置")
            if not self.model:
                raise ValueError("OPENAI_MODEL 环境变量未设置")
            
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            self._initialized = True
    
    def get_completion(self, request_params: Dict[str, Any]) -> Tuple[Any, Any]:
        """
        发送聊天完成请求并返回消息和token使用情况（非流式）
        
        Args:
            request_params: 请求参数字典，包含model, messages等
            
        Returns:
            Tuple[message, token_usage]: 返回AI助手的回复消息对象和token使用情况
        """
        request_params["model"] = self.model
        try:
            response = self.client.chat.completions.create(**request_params)
            message = response.choices[0].message
            token_usage = response.usage
            cost = getattr(token_usage, 'model_extra', {})                                                                                  
            if isinstance(cost, dict):                                                                                                      
                self._total_cost += cost.get("cost", 0)                                                                                     
            
                
            return message, token_usage
        except Exception as e:
            raise Exception(f"API请求失败: {str(e)}")
    
    def get_completion_stream(self, request_params: Dict[str, Any]) -> Generator[str, None, None]:
        """
        发送流式聊天完成请求并返回生成器，包含token使用情况
        
        Args:
            request_params: 请求参数字典，包含model, messages等
            
        Yields:
            逐步返回AI助手的回复内容片段，最后返回完整消息对象和token使用情况
        """
        request_params["model"] = self.model
        request_params["stream"] = True
        request_params["stream_options"] = {"include_usage": True}
        
        try:
            stream = self.client.chat.completions.create(**request_params)
            
            full_content = ""
            tool_calls = []
            current_tool_call = None
            token_usage = None
            
            for chunk in stream:
                # Handle token usage information
                if hasattr(chunk, 'usage') and chunk.usage:
                    token_usage = chunk.usage
                    cost = getattr(token_usage, 'model_extra', {})                                                                                  
                    if isinstance(cost, dict):                                                                                                      
                        self._total_cost += cost.get("cost", 0)   
                    continue
                
                if chunk.choices[0].delta.content:
                    content_chunk = chunk.choices[0].delta.content
                    full_content += content_chunk
                    yield content_chunk
                
                # 处理工具调用
                if hasattr(chunk.choices[0].delta, 'tool_calls') and chunk.choices[0].delta.tool_calls:
                    for tool_call_delta in chunk.choices[0].delta.tool_calls:
                        if tool_call_delta.index is not None:
                            # 确保有足够的tool_calls槽位
                            while len(tool_calls) <= tool_call_delta.index:
                                tool_calls.append({
                                    'id': None,
                                    'type': 'function',
                                    'function': {'name': None, 'arguments': ''}
                                })
                            
                            current_tool_call = tool_calls[tool_call_delta.index]
                            
                            if tool_call_delta.id:
                                current_tool_call['id'] = tool_call_delta.id
                            
                            if tool_call_delta.function:
                                if tool_call_delta.function.name:
                                    current_tool_call['function']['name'] = tool_call_delta.function.name
                                if tool_call_delta.function.arguments:
                                    current_tool_call['function']['arguments'] += tool_call_delta.function.arguments
            
            
            # 转换tool_calls为OpenAI标准格式
            formatted_tool_calls = None
            if tool_calls and any(tc['id'] for tc in tool_calls):
                formatted_tool_calls = []
                for tc in tool_calls:
                    if tc['id'] and tc['function']['name']:
                        formatted_tool_calls.append(
                            ChatCompletionMessageFunctionToolCall(
                                id=tc['id'],
                                function=Function(
                                    name=tc['function']['name'],
                                    arguments=tc['function']['arguments']
                                ),
                                type='function'
                            )
                        )
            
            # 返回标准的ChatCompletionMessage对象
            message = ChatCompletionMessage(
                content=full_content,
                role="assistant",
                tool_calls=formatted_tool_calls,
                refusal=None,
                annotations=None,
                audio=None,
                function_call=None,
                reasoning=None
            )

            # Add usage information to the message for tracking
            if token_usage:
                message.usage = token_usage
            
            yield message
            
        except Exception as e:
            raise Exception(f"流式API请求失败: {str(e)}")
