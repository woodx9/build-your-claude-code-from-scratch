import subprocess
from tools.base_agent import BaseAgent

class CmdRunner(BaseAgent):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_tool_name():
        return "cmd_runner"

    def act(self, command="", timeout=30):
        if not command:
            return "No command provided"
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    return result.stdout
                else:
                    return "Command executed successfully and no return"
            else:
                return f"Error: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            self.status = "error"
            return f"Exception: {str(e)}"

    def tool_description(self):
        return {
                "type": "function",
                "function": {
                    "name": self.get_tool_name(),
                    "description": "Execute a shell command on the system, need to require user approval before execution if this command will make a damage to user's computer. you need to make a explanation why you need to run this command.",
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "need_user_approve": {
                        "type": "boolean",
                        "description": "Whether the command requires explicit user approval before execution",
                        "default": True
                        },
                        "command": {
                        "type": "string",
                        "description": "The shell command to execute"
                        },
                        "timeout": {
                        "type": "integer",
                        "description": "Maximum number of seconds to wait for the command to finish",
                        "default": 30
                        }
                    },
                    "required": ["need_user_approve","command"]
                    }
                }
            }
    
    def get_status(self):
       return ""

