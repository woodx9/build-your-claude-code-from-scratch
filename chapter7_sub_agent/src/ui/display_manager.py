"""
Display management functionality for outputting content to users.
"""

from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from typing import Optional


class DisplayManager:
    """Manages all display operations including streaming content."""
    
    def __init__(self, console: Optional[Console] = None):
        """
        Initialize the display manager.
        
        Args:
            console: Rich console instance, creates new one if None
        """
        self._console = console or Console()
        self._live: Optional[Live] = None
        self._stream_buffer: str = ""
    
    def print_assistant_message(self, content: str, emoji: str = "🤖") -> None:
        """
        Print assistant message with markdown formatting.
        
        Args:
            content: Content to display
            emoji: Emoji to display before content
        """
        content = content.strip() if content else ""
        if content:
            if emoji:
                print(emoji)
            self._console.print(Markdown(content))
    
    def print_simple_message(self, message: str, emoji: str = "") -> None:
        """
        Print a simple message without markdown formatting.
        
        Args:
            message: Message to display
            emoji: Optional emoji to display before message
        """
        if emoji:
            print(f"{emoji} {message}")
        else:
            print(message)
    
    def start_stream_display(self, refresh_rate: int = 10) -> None:
        """
        Start streaming display mode.
        
        Args:
            refresh_rate: Refresh rate per second for live display
        """
        self._stream_buffer = ""
        self._live = Live(console=self._console, refresh_per_second=refresh_rate)
        self._live.start()
    
    def stop_stream_display(self) -> None:
        """Stop streaming display mode."""
        if self._live:
            self._live.stop()
            self._live = None
    
    def print_streaming_content(self, chunk: str) -> None:
        """
        Print streaming content chunk.
        
        Args:
            chunk: Content chunk to append and display
        """
        if not hasattr(self, "_stream_buffer"):
            self._stream_buffer = ""
        
        self._stream_buffer += chunk
        if self._live:
            self._live.update(Markdown(self._stream_buffer))
    
    def get_stream_buffer(self) -> str:
        """Get the current stream buffer content."""
        return getattr(self, "_stream_buffer", "")
    
    def clear_stream_buffer(self) -> None:
        """Clear the stream buffer."""
        self._stream_buffer = ""
    
    def print_error(self, error_message: str, emoji: str = "❌") -> None:
        """
        Print error message with special formatting.
        
        Args:
            error_message: Error message to display
            emoji: Emoji to display before error
        """
        if emoji:
            print(f"{emoji} {error_message}")
        else:
            print(error_message)
    
    def print_success(self, success_message: str, emoji: str = "✅") -> None:
        """
        Print success message with special formatting.
        
        Args:
            success_message: Success message to display
            emoji: Emoji to display before success message
        """
        if emoji:
            print(f"{emoji} {success_message}")
        else:
            print(success_message)
    
    def print_info(self, info_message: str, emoji: str = "ℹ️") -> None:
        """
        Print info message.
        
        Args:
            info_message: Info message to display
            emoji: Emoji to display before info message
        """
        if emoji:
            print(f"{emoji} {info_message}")
        else:
            print(info_message)

    def display_todos(self, todos: list, emoji: str = "📋") -> None:
        """
        Display todo list with formatting.
        
        Args:
            todos: List of todo items
            emoji: Emoji to display before todo list
        """
        if not todos:
            self.print_info("No todos to display", emoji)
            return
        
        output = []
        output.append("📋 Todo List:")
        output.append("=" * 50)
        
        for i, todo in enumerate(todos, 1):
            status_icon = self._get_status_icon(todo['status'])
            content = todo['content']
            todo_id = todo['id']
            
            output.append(f"{i:2d}. {status_icon} [{todo_id}] {content}")
        
        output.append("=" * 50)
        output.append(f"Total: {len(todos)} todos")
        
        self.print_simple_message("\n".join(output))
    
    def _get_status_icon(self, status: str) -> str:
        """
        Get icon for todo status.
        
        Args:
            status: Todo status
            
        Returns:
            Icon string for the status
        """
        icons = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅'
        }
        return icons.get(status, '❓')
