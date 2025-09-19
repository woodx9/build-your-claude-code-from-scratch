"""
Base classes and interfaces for UI components.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseInputHandler(ABC):
    """Abstract base class for input handlers."""
    
    @abstractmethod
    async def get_user_input(self, prompt: str = "Enter: ") -> str:
        """Get user input with specified prompt."""
        pass
    
    @abstractmethod
    async def wait_for_user_approval(self, content: str, emoji: str = "🤖") -> bool:
        """Wait for user approval."""
        pass


class BaseDisplayManager(ABC):
    """Abstract base class for display managers."""
    
    @abstractmethod
    def print_assistant_message(self, content: str, emoji: str = "🤖") -> None:
        """Print assistant message."""
        pass
    
    @abstractmethod
    def start_stream_display(self, refresh_rate: int = 10) -> None:
        """Start streaming display."""
        pass
    
    @abstractmethod
    def stop_stream_display(self) -> None:
        """Stop streaming display."""
        pass
    
    @abstractmethod
    def print_streaming_content(self, chunk: str) -> None:
        """Print streaming content chunk."""
        pass


class UIConfig:
    """Configuration for UI components."""
    
    def __init__(
        self,
        default_emoji_user: str = "👤",
        default_emoji_assistant: str = "🤖",
        default_emoji_error: str = "❌",
        default_emoji_success: str = "✅",
        default_emoji_info: str = "ℹ️",
        stream_refresh_rate: int = 10
    ):
        self.default_emoji_user = default_emoji_user
        self.default_emoji_assistant = default_emoji_assistant
        self.default_emoji_error = default_emoji_error
        self.default_emoji_success = default_emoji_success
        self.default_emoji_info = default_emoji_info
        self.stream_refresh_rate = stream_refresh_rate
