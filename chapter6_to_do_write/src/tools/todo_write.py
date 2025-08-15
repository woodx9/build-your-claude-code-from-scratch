import json
from tools.base_agent import BaseAgent

class TodoWrite(BaseAgent):
    def __init__(self):
        super().__init__()
        self.todos = []

    @staticmethod
    def get_tool_name():
        return "todo_write"

    def act(self, todos=None):
        if not todos:
            return "No todos provided"
        
        self.todos = todos
        return f"Successfully updated todo list with {len(todos)} todos"

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": self._tool_description(),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "todos": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "content": {
                                        "type": "string",
                                        "minLength": 1
                                    },
                                    "status": {
                                        "type": "string",
                                        "enum": [
                                            "pending",
                                            "in_progress",
                                            "completed"
                                        ]
                                    },
                                    "id": {
                                        "type": "string"
                                    }
                                },
                                "required": [
                                    "content",
                                    "status",
                                    "id"
                                ],
                                "additionalProperties": False
                            },
                            "description": "The updated todo list"
                        }
                    },
                    "required": [
                        "todos"
                    ],
                    "additionalProperties": False
                }
            }
        }
    
    def get_status(self):
        if not self.todos:
            return "No todos in memory - no todos have been added yet"
        return json.dumps({"todos": self.todos}, indent=2)

    def _tool_description(self):
        return "Stores a complete todo list in memory, replacing any existing todos."
