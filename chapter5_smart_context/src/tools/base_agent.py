from abc import abstractmethod


class BaseAgent:
    def __init__(self):
        pass

    @staticmethod
    def get_tool_name():
        return "base_agent"

    @abstractmethod
    def act(self, **kwargs):
        pass

    @abstractmethod
    def json_schema(self):
        pass

    @abstractmethod
    def get_status(self):
        pass
