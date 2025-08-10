import json
import traceback
import sys
from core.api_client import APIClient
from tools.tool_manager import ToolManager
import asyncio
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live


class Conversation:
    _instance = None
    _initialized = False
    _tool_manager = None
    _api_client = None
    _console = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Conversation, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.messages = []
            self._tool_manager = ToolManager()
            self._api_client = APIClient()
            self._initialized = True
            self._console = Console()

    async def get_user_input(self):
        """获取用户输入"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, "请输入: ")

    async def wait_for_user_input(self):
        """等待用户输入"""
        print("👤")
        user_input = await self.get_user_input()
        return user_input

    async def wait_for_user_approval(self, content: str):
        """等待用户批准"""
        print("🤖")
        print("请确认是否执行工具调用: ", content)
        print("回答 yes 或 no")
        
        while True:
            user_input = await self.get_user_input()

            if "yes" in user_input.lower():
                return True
            elif "no" in user_input.lower():
                return False
            else:
                print("无效输入，请回答 yes 或 no")

        return False

    def print_assistant_messages(self, content: str):
        """打印助手消息"""
        content = content.strip() if content else ""
        if content:
            print("🤖")
            self._console.print(Markdown(content))

    def start_stream_display(self):
            self._stream_buffer = ""
            self._live = Live(console=self._console, refresh_per_second=10)
            self._live.start()

    def stop_stream_display(self):
        if hasattr(self, "_live"):
            self._live.stop()
            del self._live

    def print_streaming_content(self, chunk: str):
        """打印流式内容片段"""
        if not hasattr(self, "_stream_buffer"):
            self._stream_buffer = ""

        self._stream_buffer += chunk
        if hasattr(self, "_live"):
            self._live.update(Markdown(self._stream_buffer))
        

    async def start_conversation(self):
        """开始新的会话"""
        self.messages = []
        self.messages.append({"role": "system", "content": "You are a helpful assistant. "})
        
        user_input = await self.wait_for_user_input()
        self.messages.append({"role": "user", "content": user_input})

        try:
            await self.recursive_message_handling()
        except Exception as e:
            print("🤖 发生系统错误：", e)
            traceback.print_exc()
            print("🤖 发生系统错误：", e)

    async def recursive_message_handling(self):
        """递归处理消息 - 支持流式输出"""
        request = {
            "messages": self.messages,
            "tools": self._tool_manager.get_tools_description(),
        }
        
        print("🤖")  # 显示助手开始回复
        
        # 使用流式API获取响应
        try:
            stream_generator = self._api_client.get_completion_stream(request)
            
            # 检查stream_generator是否为None
            if stream_generator is None:
                raise Exception("Stream generator is None - API client returned no response")
            
            response_message = None
            full_content = ""
            
            # 确保stream_generator是可迭代的
            try:
                iterator = iter(stream_generator)
            except TypeError:
                raise Exception(f"Stream generator is not iterable. Type: {type(stream_generator)}")
            
            # 开始流式打印
            self.start_stream_display() 
            # 迭代处理流式响应
            for chunk in iterator:
                if isinstance(chunk, str):
                    # 这是内容片段
                    full_content += chunk
                    self.print_streaming_content(chunk)
                else:
                    # 这是最终的消息对象
                    response_message = chunk
                    break

            # 流式输出结束
            self.stop_stream_display()
            
            # 如果没有获得完整的响应消息，创建一个
            if response_message is None:
                class SimpleMessage:
                    def __init__(self, content):
                        self.content = content
                        self.role = "assistant"
                        self.tool_calls = None
                
                response_message = SimpleMessage(full_content)
            
        except Exception as e:
            (f"\n🤖 流式响应处理出错: {e}")
            print(f"错误类型: {type(e).__name__}")
            traceback.print_exc()
            
            # 回退到非流式模式
            try:
                print("🤖 尝试使用非流式模式...")
                response_message = self._api_client.get_completion(request)
                self.print_assistant_messages(response_message.content)
            except Exception as fallback_error:
                print(f"🤖 非流式模式也失败: {fallback_error}")
                # 创建一个错误响应
                class ErrorMessage:
                    def __init__(self, error_msg):
                        self.content = f"抱歉，我遇到了技术问题: {error_msg}"
                        self.role = "assistant"
                        self.tool_calls = None
                
                response_message = ErrorMessage(str(e))
                self.print_assistant_messages(response_message.content)
                # 直接结束
                return
        
        # 将响应添加到消息历史
        self.messages.append({
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": response_message.tool_calls if hasattr(response_message, 'tool_calls') and response_message.tool_calls else None
        })

        # 处理工具调用
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls is not None and len(response_message.tool_calls) > 0:
            await self.handle_tool_calls(response_message.tool_calls)
            await self.recursive_message_handling()
        else:
            # 没有工具调用，等待用户输入
            user_input = await self.wait_for_user_input()
            self.messages.append({"role": "user", "content": user_input})
            await self.recursive_message_handling()

    async def handle_tool_calls(self, tool_calls):
        """处理工具调用"""
        for tool_call in tool_calls:
            try:
             args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                self.print_assistant_messages(f"工具参数解析失败: {e}")
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": "tool call failed due to JSONDecodeError"
                })
                continue

            # 需要用户批准
            need_user_approve = args.get('need_user_approve', False)
            should_execute = True

            if need_user_approve:
                approval_content = f"工具: {tool_call.function.name}, 参数: {args}"
                user_approval = await self.wait_for_user_approval(approval_content)
                should_execute = user_approval

            if should_execute:
                tool_args = {k: v for k, v in args.items() if k != 'need_user_approve'}
                self.print_assistant_messages(f"准备调用工具: {tool_call.function.name}, 参数: {tool_args}")
                try:
                    tool_response = self._tool_manager.run_tool(tool_call.function.name, **tool_args)
                    self.print_assistant_messages(f"成功调用工具: {tool_call.function.name}, 返回: {tool_response}")
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": json.dumps(tool_response)
                    })
                except Exception as e:
                    # 记录工具调用失败，增强程序鲁棒性
                    self.print_assistant_messages(f"调用工具失败: {tool_call.function.name}, 错误: {e}")
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": "tool call failed, fail reason: " + str(e)
                    })
            else:
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": "user denied to execute tool"
                })
