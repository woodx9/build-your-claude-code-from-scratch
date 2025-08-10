import json
import traceback
from core.api_client import APIClient
from tools.tool_manager import ToolManager
import asyncio
from rich.console import Console
from rich.markdown import Markdown


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
        """递归处理消息"""
        request = {
            "messages": self.messages,
            "tools": self._tool_manager.get_tools_description(),
        }
        response = self._api_client.get_completion(request)
        self.messages.append(response)
        self.print_assistant_messages(response.content)

        if not hasattr(response, 'tool_calls') or response.tool_calls is None or len(response.tool_calls) == 0:
            user_input = await self.wait_for_user_input()
            self.messages.append({"role": "user", "content": user_input})
            await self.recursive_message_handling()
            return

        for tool_call in response.tool_calls:
            args = json.loads(tool_call.function.arguments)
            try:
                args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                self.print_assistant_messages(f"工具参数解析失败: {e}")
                self.messages.append({"role": "tool",
                                    "name": tool_call.function.name,
                                    "content": "tool call failed due to JSONDecodeError"})
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
                    self.messages.append({"role": "tool",
                                        "tool_call_id": tool_call.id,
                                        "name": tool_call.function.name,
                                        "content": json.dumps(tool_response)
                                    })
                except Exception as e:
                    # 记录工具调用失败，增强程序鲁棒性
                    self.print_assistant_messages(f"调用工具失败: {tool_call.function.name}, 错误: {e}")
                    self.messages.append({"role": "tool",
                                          "tool_call_id": tool_call.id,
                                          "name": tool_call.function.name,
                                          "content": "tool call failed, fail reason: " + str(e)
                                          })
            else:
                self.messages.append({"role": "tool",
                                      "tool_call_id": tool_call.id,
                                      "name": tool_call.function.name,
                                      "content": "user denied to execute tool"
                                      })
                
        
        await self.recursive_message_handling()
