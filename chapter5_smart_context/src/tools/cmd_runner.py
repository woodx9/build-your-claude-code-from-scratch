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

    def json_schema(self):
        return {
                "type": "function",
                "function": {
                    "name": self.get_tool_name(),
                    "description": self._tool_description(),
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
    

    # TODO: Read and Edit file will separate as serval tools
    def _tool_description(self):
     return """
Executes a given bash command in a persistent shell session with optional timeout, user approval, and security measures.

Before executing the command, please follow these steps:
1. Security Check:
   - Always check if the command is potentially dangerous (e.g., rm, sudo, chmod 777, format, del, etc.)
   - If the command is dangerous or could cause system damage/data loss, you MUST set need_user_approve=true

2. Directory Verification:
   - If the command will create new directories or files, first use the ls command to verify the parent directory exists and is the correct location
   - For example, before running "mkdir foo/bar", first use ls to check that "foo" exists and is the intended parent directory

3. Read File Command:
   - When you need to read a file for the first time, always use `cat -n <file>` to display the contents with line numbers (default max 2000 lines)
   - For large files, consider using `head -n 100 <file>` or `tail -n 100 <file>` to preview content first

4. Edit File Command:
   - Before updating any file, you must read the file content in the current conversation first
   - When updating content in an existing file, always use sed for replacement except when the updated content is very large:
     Example: `sed "start_line,end_line c new_content" <file>`
   - When inserting content into an existing file, use sed for insertion:
     Example: `sed "insert_line_number a insert_content" <file>`
   - When searching within files, always use grep:
     Example: `grep "search_pattern" <file>`

Note: The above commands are for Linux/macOS systems. For Windows, use appropriate command-line equivalents (e.g., `dir`, `type`, PowerShell commands).

Usage notes:
  - The command and need_user_approve arguments are required.
  - You can specify an optional timeout in milliseconds (up to 120 seconds). If not specified, commands will timeout after 30 seconds.
  - Try to maintain your current working directory throughout the session by using absolute paths and avoiding usage of `cd`. You may use `cd` if the User explicitly requests it.

Committing changes with git

When the user asks you to create a new git commit, follow these steps carefully:

1. You have the capability to call multiple tools in a single response. When multiple independent pieces of information are requested, batch your tool calls together for optimal performance. ALWAYS run the following bash commands in parallel, each using the Bash tool:
  - Run a git status command to see all untracked files.
  - Run a git diff command to see both staged and unstaged changes that will be committed.
  - Run a git log command to see recent commit messages, so that you can follow this repository's commit message style.
2. Analyze all staged changes (both previously staged and newly added) and draft a commit message:
  - Summarize the nature of the changes (eg. new feature, enhancement to an existing feature, bug fix, refactoring, test, docs, etc.). Ensure the message accurately reflects the changes and their purpose (i.e. "add" means a wholly new feature, "update" means an enhancement to an existing feature, "fix" means a bug fix, etc.).
  - Check for any sensitive information that shouldn't be committed
  - Draft a concise (1-2 sentences) commit message that focuses on the "why" rather than the "what"
  - Ensure it accurately reflects the changes and their purpose
3. You have the capability to call multiple tools in a single response. When multiple independent pieces of information are requested, batch your tool calls together for optimal performance. ALWAYS run the following commands in parallel:
   - Add relevant untracked files to the staging area.
   - Run git status to make sure the commit succeeded.
4. If the commit fails due to pre-commit hook changes, retry the commit ONCE to include these automated changes. If it fails again, it usually means a pre-commit hook is preventing the commit. If the commit succeeds but you notice that files were modified by the pre-commit hook, you MUST amend your commit to include them.

Important notes:
- NEVER update the git config
- NEVER run additional commands to read or explore code, besides git bash commands
- NEVER use the TodoWrite or Task tools
- DO NOT push to the remote repository unless the user explicitly asks you to do so
- IMPORTANT: Never use git commands with the -i flag (like git rebase -i or git add -i) since they require interactive input which is not supported.
- If there are no changes to commit (i.e., no untracked files and no modifications), do not create an empty commit
- In order to ensure good formatting, ALWAYS pass the commit message via a HEREDOC, a la this example:
<example>
git commit -m "$(cat <<'EOF'
   Commit message here.
   EOF
   )"
</example>

### Creating pull requests
Use the gh command via the Bash tool for ALL GitHub-related tasks including working with issues, pull requests, checks, and releases. If given a Github URL use the gh command to get the information needed.

IMPORTANT: When the user asks you to create a pull request, follow these steps carefully:

1. You have the capability to call multiple tools in a single response. When multiple independent pieces of information are requested, batch your tool calls together for optimal performance. ALWAYS run the following bash commands in parallel using the Bash tool, in order to understand the current state of the branch since it diverged from the main branch:
   - Run a git status command to see all untracked files
   - Run a git diff command to see both staged and unstaged changes that will be committed
   - Check if the current branch tracks a remote branch and is up to date with the remote, so you know if you need to push to the remote
   - Run a git log command and `git diff [base-branch]...HEAD` to understand the full commit history for the current branch (from the time it diverged from the base branch)
2. Analyze all changes that will be included in the pull request, making sure to look at all relevant commits (NOT just the latest commit, but ALL commits that will be included in the pull request!!!), and draft a pull request summary
3. You have the capability to call multiple tools in a single response. When multiple independent pieces of information are requested, batch your tool calls together for optimal performance. ALWAYS run the following commands in parallel:
   - Create new branch if needed
   - Push to remote with -u flag if needed
   - Create PR using gh pr create with the format below. Use a HEREDOC to pass the body to ensure correct formatting.
<example>
gh pr create --title "the pr title" --body "$(cat <<'EOF'
#### Summary
<1-3 bullet points>

Important:
- NEVER update the git config
""".strip()
