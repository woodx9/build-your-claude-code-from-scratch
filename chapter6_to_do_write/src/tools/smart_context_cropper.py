import subprocess
from core.history.history_manager import Crop_Direction, HistoryManager
from tools.base_agent import BaseAgent

class SmartContextCropper(BaseAgent):
    def __init__(self):
        super().__init__()
        self._history_manager = HistoryManager()

    @staticmethod
    def get_tool_name():
        return "smart_context_cropper"

    def act(self, crop_direction: Crop_Direction, crop_amount: int, deleted_messages_summary: str):
        try:
            if (crop_amount <= 0):
                return "Invalid crop amount. It must be positive."
            result = self._history_manager.crop_message(crop_direction, crop_amount)
            return result
        except Exception as e:
            return f"smart_context_cropper run Error: {e}"

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
                            "description": "Whether the crop messages action requires explicit user approval before execution",
                            "default": True
                        },
                        "crop_direction": {
                            "type": "string",
                            "enum": ["top", "bottom"],
                            "description": "Direction to crop messages. 'top' removes messages from the start (after system message), 'bottom' removes from the end."
                        },
                        "crop_amount": {
                            "type": "integer",
                            "minimum": 1,
                            "description": "Number of messages to remove. Must not exceed the allowed limit for preserving the latest user message."
                        },
                        "deleted_messages_summary": {
                            "type": "string",
                            "description": "Summary of the deleted messages."
                        }
                    },
                    "required": ["need_user_approve", "crop_direction", "crop_amount", "deleted_messages_summary"]
                    }
                }
            }
    
    def get_status(self):
       return ""
    
    def _tool_description(self):
        return """
Crop conversation history from either the top (after system messages) or the bottom, while ensuring the latest user message is never removed.

Before executing smart_context_cropper, follow these steps:
1. Crop Rules
    - Always preserve the latest user message.
    - Top crop → remove the oldest non-system messages that appear after the system message.
    - Bottom crop → remove the most recent messages first.

2. Approval Requirements
    - Always consider the user's current task.
    - If you are certain that the messages to be cropped are unrelated to the user's current task, you may proceed without explicit approval.
    - If there is any uncertainty, request confirmation before cropping.

3. Handling Removed Content
    - If cropped messages contain useful information, provide a concise summary before deletion.
    - Ensure summaries retain any context that might still be relevant to the user's ongoing task.
    - If Nothing useful related in deleted message, than deleted_messages_summary will be empty.

<example>
system_prompt: You are a professional programming assistant.
user_message: Write a Python function to compute the Fibonacci sequence.
assistant: Here's’s the basic version...
user_message: Please optimize the performance.
assistant: Here’s the optimized version...
</example>
<smart_context_cropper>
smart_context_cropper(
    need_user_approve = true,
    crop_direction = "TOP",
    crop_amount = 2,
)
</smart_context_cropper>

<example>
system_prompt: You are a professional debugging assistant.
user_message: Diagnose the midnight latency spikes in our API.
assistant: I will explore a few hypotheses...
assistant: Attempt 1: Enabled verbose logging and observed long GC pauses; tuned GC, but latency stayed high.
assistant: Attempt 2: Investigated DB write locks; added an index to the hot table; no measurable improvement.
assistant: Attempt 3: Correlated spikes with a batch job; disabled an experiment, but the spikes persisted.
# Once the failures are summarized, the detailed attempt logs can be removed from the bottom to keep context focused.
</example>
<smart_context_cropper>
smart_context_cropper(
    need_user_approve = false,
    crop_direction = "BOTTOM",
    crop_amount = 3,
    deleted_messages_summary = "Failure summary: (1) GC tuning ineffective despite observed long pauses; (2) DB write-lock hypothesis invalid—adding index did not reduce latency; (3) Batch-job correlation inconclusive—disabling related experiment had no effect. Conclusion: Spikes likely due to overlap of scheduled tasks with DB maintenance. Next steps: inspect cron jobs at 00:00 and DB vacuum/backup windows; add temporary rate-limiting or queueing around that window."
)
</smart_context_cropper>

</examples>
    """.strip()