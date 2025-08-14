from tools.cmd_runner import CmdRunner
from tools.smart_context_cropper import SmartContextCropper

class ToolManager:
    def __init__(self):
        self.tools = {}
        # Important tools should be placed lower, as this affects their position in the prompt.
        self._register_tool(SmartContextCropper.get_tool_name(), SmartContextCropper())
        self._register_tool(CmdRunner.get_tool_name(), CmdRunner())   

    def _register_tool(self, name, tool_instance):
        self.tools[name] = tool_instance

    def get_tools_description(self):
        descriptions = []
        for tool_name, tool_instance in self.tools.items():
            descriptions.append(tool_instance.json_schema())
        return descriptions
    
    # TODO： 数组越界直接再次抛出异常
    def run_tool(self, tool_name, **kwargs):
        tool = self.tools.get(tool_name)
        try:
            if tool:
                return tool.act(**kwargs)
        except Exception as e:
            return f"Error occurred while running tool '{tool_name}': {str(e)}"
        return "Tool not found"
