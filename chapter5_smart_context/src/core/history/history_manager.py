from abc import ABC, abstractmethod
import copy
from dataclasses import dataclass
import os
from pyexpat.errors import messages
from dotenv import load_dotenv
from ui.ui_manager import UIManager
from enum import Enum

# 加载环境变量
load_dotenv()

@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int

from enum import Enum

class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    TOOL = "tool"
    ASSISTANT = "assistant"

class Crop_Direction(str, Enum):
    TOP = "top"
    BOTTOM = "bottom"

class BaseHistoryManager(ABC):
    def __init__(self):
        self.messages_history = [[]]
        self.history_token_usage = []

    @abstractmethod
    def add_message(self, message) -> None:
        pass

    @abstractmethod
    def update_token_usage(self, token_usage) -> None:
        pass

    @abstractmethod
    def get_current_messages(self) -> any:
        pass

    def auto_messages_compression(self) -> None:
        if self._requires_compression():
            self._compress_current_message()

    @abstractmethod
    def _requires_compression(self) -> bool:
        pass

    @abstractmethod
    def _compress_current_message(self) -> None:
        pass


class HistoryManager(BaseHistoryManager):
    _instance = None
    _initialized = False
    
    def __new__(cls, model_max_tokens: int = 200, compress_threshold: float = 0.8):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, model_max_tokens: int = 200, compress_threshold: float = 0.8):
        if not self._initialized:
            super().__init__()
            self._ui_manager = UIManager()
            self._model_max_tokens =  int(os.getenv("MODEL_MAX_TOKENS", model_max_tokens)) * 1024
            self._compress_threshold = float(os.getenv("COMPRESS_THRESHOLD", compress_threshold))
            self._initialized = True

    def add_message(self, message) -> None:
        self.messages_history[-1].append(message)

    # mustn't crop the latest user input message
    # mustn't crop_amount < current_messages - 1 
    def crop_message(self, crop_direction: Crop_Direction, crop_amount: int) -> str:  
        current_messages = self.messages_history[-1]
        
        if len(current_messages) <= 1:
            return "Cannot crop: insufficient messages"
        
        if len(current_messages) < crop_amount + 2:
            return "Cannot crop: invalid crop amount"

        # find the latest user message index
        latest_user_index = -1
        for i in range(len(current_messages) - 1, -1, -1):
            if current_messages[i]['role'] == Role.USER:
                latest_user_index = i
                break
        
        if latest_user_index == -1:
            return "Cannot crop: no user messages found"

        # ensure not to crop the latest user input message
        if crop_direction == Crop_Direction.TOP:
            max_crop_amount = latest_user_index
        else:  # BOTTOM
            max_crop_amount = len(current_messages) - latest_user_index - 1
            
        
        if crop_amount >  max_crop_amount:
            return "Cannot crop: can't crop the latest user message"

        if crop_direction == Crop_Direction.TOP:
            # crop from the top, keeping system messages and content after the latest user message
            system_messages = [msg for msg in current_messages if msg['role'] == Role.SYSTEM]
            cropped_messages = system_messages + current_messages[crop_amount:]
        else:  # BOTTOM
            # crop from the bottom, ensuring not to crop the latest user message
            cropped_messages = current_messages[:-crop_amount]
        
        self.messages_history[-1] = cropped_messages
        return "Crop message successful"

    @property                                                                                                                       
    def current_context_window(self):                                                                                               
        """get current context window usage percentage"""                                                                           
        if not self.history_token_usage or self._model_max_tokens == 0:                                                             
            return "0.0"                                                                                                            
        return f"{100 * self.history_token_usage[-1].total_tokens / self._model_max_tokens:.1f}" 

    def update_token_usage(self, token_usage) -> None:
        token_usage = TokenUsage(
            input_tokens = token_usage.prompt_tokens,
            output_tokens = token_usage.completion_tokens,
            total_tokens = token_usage.total_tokens
        )

        if len(self.history_token_usage) == 0:
            self.history_token_usage.append(token_usage)
        else:
            self.history_token_usage[-1] = token_usage

    def get_current_messages(self) -> any:
        return  copy.deepcopy(self.messages_history[-1])

    def _requires_compression(self) -> bool:
        if self._compress_threshold and self.history_token_usage:
            current_usage = self.history_token_usage[-1]
            return current_usage.total_tokens > self._compress_threshold * self._model_max_tokens
        return False

    # if there is more than one  session, compress the oldest chat session
    # else compress the current roll assistant output
    # tell the model we have compressed the messages
    def _compress_current_message(self) -> None:
        """压缩当前消息历史以节省上下文窗口空间"""
        self._ui_manager.print_assistant_message("历史上下文过长，正在压缩中...")

        current_messages = self.messages_history[-1]
        user_indices = self._get_user_message_indices(current_messages)
        
        if len(user_indices) > 1:
            self._compress_multiple_sessions(current_messages, user_indices)
        elif len(user_indices) == 1:
            # delete_message_num is hardcode to 3 right now
            self._compress_single_session(current_messages, user_indices[0], 3)
    
    def _get_user_message_indices(self, messages: list) -> list[int]:
        """获取所有用户消息的索引位置"""
        return [i for i, msg in enumerate(messages) if msg.role == Role.USER]
    
    def _compress_multiple_sessions(self, messages: list, user_indices: list[int]) -> None:
        """delete the oldest chat session"""
        second_oldest_user_index = user_indices[1]

        system_messages = [msg for msg in messages[:second_oldest_user_index] if msg.role == Role.SYSTEM]
        recent_messages = messages[second_oldest_user_index:]

        self.messages_history[-1] = system_messages + self._create_compression_notice(messages) + recent_messages

    def _compress_single_session(self, messages: list, user_index: int, delete_message_num: int) -> None:
        """delete assistant messages and tool message close to user input"""
        system_messages = [msg for msg in messages[:user_index] if msg.role == Role.SYSTEM]
        
        start_index = min(user_index + 1 + delete_message_num, len(messages))
        user_message = [messages[user_index]] + self._create_compression_notice(messages) + messages[start_index:]

        self.messages_history[-1] = system_messages + user_message

    def _create_compression_notice(self, messages: list) -> list:
        """create compression notice"""
        if not messages:
            return []
        
        message_class = type(messages[0])
        compression_notice = message_class(
            role=Role.USER,
            content="[Previous conversation history has been compressed to save context window space]"
        )
        return [compression_notice]
            
