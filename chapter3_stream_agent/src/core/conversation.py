"""
Conversation management with refactored UI components.
"""

import json
import traceback
from core.api_client import APIClient
from tools.tool_manager import ToolManager
from ui.ui_manager import UIManager


class Conversation:
    """
    Main conversation class that handles the chat flow and tool interactions.
    UI responsibilities have been extracted to the UIManager.
    """
    
    _instance = None
    _initialized = False
    _tool_manager = None
    _api_client = None
    _ui_manager = None

    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super(Conversation, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the conversation with required managers."""
        if not self._initialized:
            self.messages = []
            self._tool_manager = ToolManager()
            self._api_client = APIClient()
            self._ui_manager = UIManager()
            self._initialized = True

    async def start_conversation(self):
        """Start a new conversation."""
        self.messages = []
        self.messages.append({"role": "system", "content": "You are a helpful assistant. "})
        
        user_input = await self._ui_manager.get_user_input()
        self.messages.append({"role": "user", "content": user_input})

        try:
            await self._recursive_message_handling()
        except Exception as e:
            self._ui_manager.print_error(f"发生系统错误：{e}")
            traceback.print_exc()

    async def _recursive_message_handling(self):
        """
        Recursively handle messages with streaming support.
        This is the main conversation loop.
        """
        request = {
            "messages": self.messages,
            "tools": self._tool_manager.get_tools_description(),
        }
        
        # Start assistant response
        self._ui_manager.print_simple_message("", "🤖")
        
        # Use streaming API for response
        try:
            stream_generator = self._api_client.get_completion_stream(request)
            
            # Validate stream generator
            if stream_generator is None:
                raise Exception("Stream generator is None - API client returned no response")
            
            response_message = None
            full_content = ""
            
            # Ensure stream_generator is iterable
            try:
                iterator = iter(stream_generator)
            except TypeError:
                raise Exception(f"Stream generator is not iterable. Type: {type(stream_generator)}")
            
            # Start streaming display
            self._ui_manager.start_stream_display()
            
            # Process streaming response
            for chunk in iterator:
                if isinstance(chunk, str):
                    # This is content chunk
                    full_content += chunk
                    self._ui_manager.print_streaming_content(chunk)
                else:
                    # This is the final message object
                    response_message = chunk
                    break

            # End streaming display
            self._ui_manager.stop_stream_display()
            
            # If no complete response message, create one
            if response_message is None:
                response_message = self._create_simple_message(full_content)
            
        except Exception as e:
            self._ui_manager.print_error(f"流式响应处理出错: {e}")
            self._ui_manager.print_info(f"错误类型: {type(e).__name__}")
            traceback.print_exc()
            
            # Fallback to non-streaming mode
            try:
                self._ui_manager.print_info("尝试使用非流式模式...")
                response_message = self._api_client.get_completion(request)
                self._ui_manager.print_assistant_message(response_message.content)
            except Exception as fallback_error:
                self._ui_manager.print_error(f"非流式模式也失败: {fallback_error}")
                # Create error response
                response_message = self._create_error_message(str(e))
                self._ui_manager.print_assistant_message(response_message.content)
                return
        
        # Add response to message history
        self.messages.append({
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": response_message.tool_calls if hasattr(response_message, 'tool_calls') and response_message.tool_calls else None
        })

        # Handle tool calls
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls is not None and len(response_message.tool_calls) > 0:
            await self._handle_tool_calls(response_message.tool_calls)
            await self._recursive_message_handling()
        else:
            # No tool calls, wait for user input
            user_input = await self._ui_manager.get_user_input()
            self.messages.append({"role": "user", "content": user_input})
            await self._recursive_message_handling()

    async def _handle_tool_calls(self, tool_calls):
        """Handle tool calls with user approval when needed."""
        for tool_call in tool_calls:
            try:
                args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                self._ui_manager.print_error(f"工具参数解析失败: {e}")
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": "tool call failed due to JSONDecodeError"
                })
                continue

            # Check if user approval is needed
            need_user_approve = args.get('need_user_approve', False)
            should_execute = True

            if need_user_approve:
                approval_content = f"工具: {tool_call.function.name}, 参数: {args}"
                should_execute = await self._ui_manager.wait_for_user_approval(approval_content)

            if should_execute:
                await self._execute_tool(tool_call, args)
            else:
                self._add_tool_response(tool_call, "user denied to execute tool")

    async def _execute_tool(self, tool_call, args):
        """Execute a tool call and handle the response."""
        tool_args = {k: v for k, v in args.items() if k != 'need_user_approve'}
        self._ui_manager.show_preparing_tool(tool_call.function.name, tool_args)
        
        try:
            tool_response = self._tool_manager.run_tool(tool_call.function.name, **tool_args)
            self._ui_manager.show_tool_execution(
                tool_call.function.name, 
                tool_args, 
                success=True, 
                result=str(tool_response)
            )
            self._add_tool_response(tool_call, json.dumps(tool_response))
        except Exception as e:
            # Enhanced error handling for tool execution
            self._ui_manager.show_tool_execution(
                tool_call.function.name, 
                tool_args, 
                success=False, 
                result=str(e)
            )
            self._add_tool_response(tool_call, f"tool call failed, fail reason: {str(e)}")

    def _add_tool_response(self, tool_call, content):
        """Add tool response to message history."""
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": content
        })

    def _create_simple_message(self, content):
        """Create a simple message object."""
        class SimpleMessage:
            def __init__(self, content):
                self.content = content
                self.role = "assistant"
                self.tool_calls = None
        
        return SimpleMessage(content)

    def _create_error_message(self, error_msg):
        """Create an error message object."""
        class ErrorMessage:
            def __init__(self, error_msg):
                self.content = f"抱歉，我遇到了技术问题: {error_msg}"
                self.role = "assistant"
                self.tool_calls = None
        
        return ErrorMessage(error_msg)
