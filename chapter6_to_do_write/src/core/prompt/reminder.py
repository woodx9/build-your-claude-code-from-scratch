from tools.todo_write import TodoWrite

def get_reminder() -> str:
    todo_tool = TodoWrite()
    todo_status = todo_tool.get_status()
    
    return f"""
## Current Todo Status
{todo_status}

Remember to check and update your todos regularly to stay organized and productive.
""".strip()
