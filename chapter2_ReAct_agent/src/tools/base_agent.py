class BaseAgent:
    def __init__(self):
        pass

    @staticmethod
    def get_tool_name():
        return "base_agent"

    def act(self, **kwargs):
        pass

    def get_prompt(self):
        pass

    def get_status(self):
        pass
