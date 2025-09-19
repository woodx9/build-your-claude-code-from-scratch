from tools.cmd_runner import CmdRunner
from tools.smart_context_cropper import SmartContextCropper
from tools.task import Task
from tools.todo_write import TodoWrite

class ToolManager:
    _instance = None
    _initialized = False
    _mcp_client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.tools = {}
            # Important tools should be placed lower, as this affects their position in the prompt.
            self._register_tool(SmartContextCropper.get_tool_name(), SmartContextCropper())
            self._register_tool(TodoWrite.get_tool_name(), TodoWrite()) 
            self._register_tool(Task.get_tool_name(), Task())
            self._register_tool(CmdRunner.get_tool_name(), CmdRunner())   
            ToolManager._initialized = True

    def _register_tool(self, name, tool_instance):
        self.tools[name] = tool_instance

    def get_tools_description(self):
        descriptions = []
        for tool_name, tool_instance in self.tools.items():
            descriptions.append(tool_instance.json_schema())
        return descriptions
    
    # TODO：Array out of bounds should directly throw exception again
    async def run_tool(self, tool_name, **kwargs):
        tool = self.tools.get(tool_name)
        try:
            if tool:
                return await tool.act(**kwargs)
        except Exception as e:
            return f"Error occurred while running tool '{tool_name}': {str(e)}"
        return "Tool not found"

    def get_tool_status(self, tool_name):
        tool = self.tools.get(tool_name)
        if tool:
            return tool.get_status()
        return "Tool not found"
