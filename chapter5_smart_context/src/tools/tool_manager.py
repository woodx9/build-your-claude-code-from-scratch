from tools.cmd_runner import CmdRunner

class ToolManager:
    def __init__(self):
        self.tools = {}
        self.register_tool(CmdRunner.get_tool_name(), CmdRunner())

    def register_tool(self, name, tool_instance):
        self.tools[name] = tool_instance

    def get_tools_description(self):
        descriptions = []
        for tool_name, tool_instance in self.tools.items():
            descriptions.append(tool_instance.tool_description())
        return descriptions
    
    def run_tool(self, tool_name, **kwargs):
        tool = self.tools.get(tool_name)
        if tool:
            return tool.act(**kwargs)
        return "Tool not found"
