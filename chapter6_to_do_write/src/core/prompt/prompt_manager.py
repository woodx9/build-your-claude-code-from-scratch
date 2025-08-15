from abc import ABC, abstractmethod

from core.prompt.enviroment import get_enviroment_info
from core.prompt.system_rule import get_system_rule


class BasePromptManager(ABC):

    @abstractmethod
    def get_system_prompt(self) -> None:
        pass



class PromptManager(BasePromptManager):
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True

    def get_system_prompt(self) -> str:
        return f"""
        {get_system_rule()}
        {get_enviroment_info()}
        """.strip()