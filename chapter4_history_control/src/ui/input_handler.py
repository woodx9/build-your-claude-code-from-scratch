"""
Input handling functionality for user interactions.
"""

import asyncio
from typing import Optional


class InputHandler:
    """Handles all user input operations."""
    
    def __init__(self):
        """Initialize the input handler."""
        pass
    
    async def get_user_input(self, prompt: str = "请输入: ") -> str:
        """
        Get user input asynchronously.
        
        Args:
            prompt: The prompt to display to the user
            
        Returns:
            User input as string
        """
        print("👤")
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, prompt)

    
    async def wait_for_user_approval(self, content: str, emoji: str = "🤖") -> bool:
        """
        Wait for user approval (yes/no) for a specific action.
        
        Args:
            content: Content to display for approval
            emoji: Emoji to display before the approval request
            
        Returns:
            True if user approves, False otherwise
        """
        if emoji:
            print(emoji)
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
    
    async def get_choice_input(self, prompt: str, choices: list, case_sensitive: bool = False) -> Optional[str]:
        """
        Get user input with predefined choices.
        
        Args:
            prompt: The prompt to display
            choices: List of valid choices
            case_sensitive: Whether the choice matching is case sensitive
            
        Returns:
            The chosen option or None if invalid
        """
        print(prompt)
        print(f"可选项: {', '.join(choices)}")
        
        user_input = await self.get_user_input()
        
        if not case_sensitive:
            user_input = user_input.lower()
            choices = [choice.lower() for choice in choices]
        
        if user_input in choices:
            return user_input
        return None
