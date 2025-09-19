"""
Main UI manager that coordinates input and display operations.
"""

from typing import Optional
from rich.console import Console
from .input_handler import InputHandler
from .display_manager import DisplayManager


class UIManager:
    """
    Main UI manager that provides a unified interface for all UI operations.
    This class coordinates between input handling and display management.
    """
    
    _instance: Optional['UIManager'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'UIManager':
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super(UIManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, console: Optional[Console] = None):
        """
        Initialize the UI manager with input handler and display manager.
        
        Args:
            console: Rich console instance, creates new one if None
        """
        if not self._initialized:
            self._console = console or Console()
            self.input_handler = InputHandler()
            self.display_manager = DisplayManager(self._console)
            self._initialized = True
    
    # Input delegation methods
    async def get_user_input(self, prompt: str = "Enter: ") -> str:
        """Get user input with specified prompt."""
        return await self.input_handler.get_user_input(prompt)
    
    async def wait_for_user_approval(self, content: str, emoji: str = "🤖") -> tuple[bool, str]:
        """Wait for user approval with optional denial message."""
        return await self.input_handler.wait_for_user_approval(content, emoji)
    
    async def get_choice_input(self, prompt: str, choices: list, case_sensitive: bool = False) -> Optional[str]:
        """Get user input with predefined choices."""
        return await self.input_handler.get_choice_input(prompt, choices, case_sensitive)
    
    # Display delegation methods
    def print_assistant_message(self, content: str, emoji: str = "🤖") -> None:
        """Print assistant message with markdown formatting."""
        self.display_manager.print_assistant_message(content, emoji)
    
    def print_simple_message(self, message: str, emoji: str = "") -> None:
        """Print simple message without markdown formatting."""
        self.display_manager.print_simple_message(message, emoji)
    
    def print_error(self, error_message: str, emoji: str = "❌") -> None:
        """Print error message."""
        self.display_manager.print_error(error_message, emoji)
    
    def print_success(self, success_message: str, emoji: str = "") -> None:
        """Print success message."""
        self.display_manager.print_success(success_message, emoji)
    
    def print_info(self, info_message: str, emoji: str = "") -> None:
        """Print info message."""
        self.display_manager.print_info(info_message, emoji)
    
    # Streaming methods
    def start_stream_display(self, refresh_rate: int = 10) -> None:
        """Start streaming display mode."""
        self.display_manager.start_stream_display(refresh_rate)
    
    def stop_stream_display(self) -> None:
        """Stop streaming display mode."""
        self.display_manager.stop_stream_display()
    
    def print_streaming_content(self, chunk: str) -> None:
        """Print streaming content chunk."""
        self.display_manager.print_streaming_content(chunk)
    
    def get_stream_buffer(self) -> str:
        """Get current stream buffer content."""
        return self.display_manager.get_stream_buffer()
    
    def clear_stream_buffer(self) -> None:
        """Clear the stream buffer."""
        self.display_manager.clear_stream_buffer()
    
    # Convenience methods that combine input and display
    async def confirm_action(self, action_description: str) -> tuple[bool, str]:
        """
        Show action description and ask for confirmation.
        
        Args:
            action_description: Description of the action to confirm
            
        Returns:
            Tuple of (approval_status, denial_message)
        """
        return await self.wait_for_user_approval(action_description)
    
    def show_tool_execution(self, tool_name: str, tool_args: dict, success: bool = True, result: str = "") -> None:
        """
        Display tool execution information.
        
        Args:
            tool_name: Name of the tool being executed
            tool_args: Arguments passed to the tool
            success: Whether the execution was successful
            result: Result of the execution
        """
        if success:
            self.print_success(f"Successfully called tool: {tool_name}, args: {tool_args}, result: {result}")
        else:
            self.print_error(f"Tool call failed: {tool_name}, error: {result}")
    
    def show_preparing_tool(self, tool_name: str, tool_args: dict) -> None:
        """
        Show that a tool is being prepared for execution.
        
        Args:
            tool_name: Name of the tool
            tool_args: Arguments for the tool
        """
        self.print_info(f"Preparing to call tool: {tool_name}, args: {tool_args}")
    
    # Todo display delegation method
    def display_todos(self, todos: list, emoji: str = "📋") -> None:
        """Display todo list with formatting."""
        self.display_manager.display_todos(todos, emoji)
