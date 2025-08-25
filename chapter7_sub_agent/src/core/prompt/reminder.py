from tools.todo_write import TodoWrite
from tools.tool_manager import ToolManager

def get_reminder() -> str:
    tool_manager = ToolManager()
    todo_status = tool_manager.get_tool_status(TodoWrite.get_tool_name())

    return f"""
<reminder>
## Current Todo Status
{todo_status}
Remember to check and update your todos using tool todo_write regularly to stay organized and productive.
</reminder>
""".strip()
