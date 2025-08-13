# adapt from Claude Code
import os
import platform
from pathlib import Path
from datetime import datetime

def get_working_directory():
    """Get the current working directory"""
    return f"Working directory: {os.getcwd()}"

def check_git_repository():
    """Check if current directory is a git repository"""
    current_dir = Path(os.getcwd())
    
    # Check current directory and parent directories for .git folder
    for path in [current_dir] + list(current_dir.parents):
        git_dir = path / '.git'
        if git_dir.exists():
            return f"Is directory a git repo: Yes, In {path} git repository"
    
    return "Is directory a git repo: No"

def get_platform():
    """Get the current platform"""
    return f"Platform: {platform.system().lower()}"

def get_os_version():
    """Get the OS version information"""
    return f"OS Version: {platform.platform()}"

def get_current_date():
    """Get today's date"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"Today's date: {today}"

def get_enviroment_info():
    """Get all environment information as a formatted string"""
    info_parts = [
        get_working_directory(),
        check_git_repository(),
        get_platform(),
        get_os_version(),
        get_current_date()
    ]
    return "\n".join(info_parts)