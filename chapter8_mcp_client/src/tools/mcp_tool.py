import json
from tools.base_tool import BaseTool
from mcp import ClientSession, Tool

class McpTool(BaseTool):
    def __init__(self, tool: Tool, session: ClientSession):
        super().__init__()
        self.session = session
        self.tool = tool

    @staticmethod
    def get_tool_name():
        return ""

    async def act(self, **kwargs):
        try:
            response =  await self.session.call_tool(self.tool.name, kwargs)
            return response.content
        except Exception as e:
            return f"Mcp Tool {self.tool.name} run Error: {e}"

    def json_schema(self):
        return {
                "type": "function",
                "function": {
                    "name": self.tool.name,
                    "description": self.tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": self.tool.inputSchema.get("properties", {}),
                        "required": self.tool.inputSchema.get("required", {})
                    }
                }
        }
    
    def get_status(self):
       return ""
    
    def _tool_description(self):
        return ""
