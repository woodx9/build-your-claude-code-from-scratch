from tools.base_tool import BaseTool
from tools.subagent.subagent_manager import SubagentManager
from ui.ui_manager import UIManager


class Task(BaseTool):
    def __init__(self):
        super().__init__()
        self.todos = []
        self._ui_manager = UIManager()
        self._has_initialized_task = False
        self._subagent_manager = SubagentManager()

    @staticmethod
    def get_tool_name():
        return "task"

    async def act(self, description, prompt, subagent_type):
        if len(prompt) == 0:
            return "Prompt is empty"
        if len(subagent_type) == 0:
            return "Subagent type is empty"
        self._has_initialized_task = True

        from core.conversation import Conversation
        conversation = Conversation()

        self._ui_manager.print_info(f"Submitting task to {subagent_type} sub-agent: {description}\n Prompt: {prompt}")
        subagent_system_prompt = self._subagent_manager.get_subagent_prompt(subagent_type)
        response = await conversation.start_task(task_system_prompt=subagent_system_prompt, user_input=prompt)

        self._has_initialized_task = False
        return f"Task Finished with response: {response}"

    def json_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.get_tool_name(),
                "description": self._tool_description(),
                "parameters": {
                        "type": "object",
                        "properties": {
                        "description": {
                            "type": "string",
                            "description": "A short (3-5 word) description of the task"
                        },
                        "prompt": {
                            "type": "string",
                            "description": "The task for the agent to perform"
                        },
                        "subagent_type": {
                            "type": "string",
                            "description": "The type of specialized agent to use for this task"
                        }
                    },
                    "required": ["description", "prompt", "subagent_type"],
                }
            }
        }
    
    def get_status(self):
       return ""
    

    def _tool_description(self):
     return """
Launch a new agent to handle complex, multi-step tasks autonomously. 

Available agent types and the tools they have access to:
- general-purpose: General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks. When you are searching for a keyword or file and are not confident that you will find the right match in the first few tries use this agent to perform the search for you. (Tools: *)

When using the Task tool, you must specify a subagent_type parameter to select which agent type to use.

When NOT to use the Agent tool:
- When you want to read a specific file path
- When you are searching for a specific class definition like "class Foo"
- When you are searching for code within a specific file or set of 2-3 files
- Other tasks that are not related to the agent descriptions above

Usage notes:
1. Launch multiple agents concurrently whenever possible, to maximize performance; to do that, use a single message with multiple tool uses
2. When the agent is done, it will return a single message back to you. The result returned by the agent is not visible to the user. To show the user the result, you should send a text message back to the user with a concise summary of the result.
3. Each agent invocation is stateless. You will not be able to send additional messages to the agent, nor will the agent be able to communicate with you outside of its final report. Therefore, your prompt should contain a highly detailed task description for the agent to perform autonomously and you should specify exactly what information the agent should return back to you in its final and only message to you.
4. The agent's outputs should generally be trusted
5. Clearly tell the agent whether you expect it to write code or just to do research (search, file reads, etc.), since it is not aware of the user's intent
6. If the agent description mentions that it should be used proactively, then you should try your best to use it without the user having to ask for it first. Use your judgement.

Example usage:

<example_agent_descriptions>
"code-reviewer": use this agent after you are done writing a signficant piece of code
"greeting-responder": use this agent when to respond to user greetings with a friendly joke
</example_agent_description>

<example>
user: "Please write a function that checks if a number is prime"
assistant: Sure let me write a function that checks if a number is prime
assistant: First let me use the Write tool to write a function that checks if a number is prime
assistant: I'm going to use the Write tool to write the following code:
<code>
function isPrime(n) {
  if (n <= 1) return false
  for (let i = 2; i * i <= n; i++) {
    if (n % i === 0) return false
  }
  return true
}
</code>
<commentary>
Since a signficant piece of code was written and the task was completed, now use the code-reviewer agent to review the code
</commentary>
assistant: Now let me use the code-reviewer agent to review the code
assistant: Uses the Task tool to launch the with the code-reviewer agent 
</example>

<example>
user: "Hello"
<commentary>
Since the user is greeting, use the greeting-responder agent to respond with a friendly joke
</commentary>
assistant: "I'm going to use the Task tool to launch the with the greeting-responder agent"
</example>
        """.strip()