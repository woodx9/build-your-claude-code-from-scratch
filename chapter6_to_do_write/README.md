# QuickStar - Smart Context Agent

[中文版本](./README_zh.md)

A ReAct (Reasoning and Acting) based AI agent system with real-time streaming, intelligent history management, cost tracking, smart context cropping, and structured task management.

## 🚀 What's New in Chapter 6

Chapter 6 introduces the **TodoWrite Tool** - an intelligent task management system that automatically organizes complex workflows into structured todo lists with real-time progress tracking.

### Key Benefits
- **Automated Organization**: Converts complex requests into structured task lists
- **Progress Visibility**: Real-time tracking of task completion status  
- **Quality Assurance**: Prevents marking tasks complete until all requirements are met
- **Context Awareness**: Intelligently decides when todo lists add value

## 🛠️ TodoWrite Tool

### Core Features
- **Task States**: `pending` → `in_progress` → `completed`
- **Smart Detection**: Automatically activates for multi-step tasks (3+ operations)
- **Single Focus**: Only one task can be `in_progress` at a time
- **Completion Validation**: Tasks marked complete only when tests pass and requirements are fully met

### When It Activates
```bash
# Multi-step feature requests
User: "Add dark mode toggle, run tests, and build the app"
→ Creates structured todo list automatically

# Multiple feature requests  
User: "Implement user registration, product catalog, shopping cart"
→ Breaks down into organized subtasks

# Complex debugging workflows
User: "Fix the API latency issues and optimize performance"
→ Creates systematic investigation plan
```

### Usage Examples

**Feature Development**:
```python
# Automatically created for complex features
[
  {"content": "Create authentication API endpoints", "status": "pending"},
  {"content": "Build login/register UI components", "status": "pending"}, 
  {"content": "Implement session management", "status": "pending"},
  {"content": "Add security middleware and tests", "status": "pending"}
]
```

**Bug Fix Workflow**:
```python
# Systematic debugging approach
[
  {"content": "Reproduce issue in development", "status": "in_progress"},
  {"content": "Identify root cause", "status": "pending"},
  {"content": "Implement fix with tests", "status": "pending"},
  {"content": "Validate in staging", "status": "pending"}
]
```

## 📊 Feature Evolution

| Capability | Chapter 4 | Chapter 5 | Chapter 6 |
|------------|-----------|-----------|-----------|
| Streaming Output | ✅ | ✅ | ✅ |
| History Management | ✅ | ✅ | ✅ |
| Smart Cropping | ❌ | ✅ | ✅ |
| User Interaction | Basic | Enhanced | Enhanced |
| **Task Management** | ❌ | ❌ | **✅ TodoWrite** |
| **Progress Tracking** | Manual | Manual | **✅ Automated** |

## 🧪 Testing

```bash
# Test TodoWrite functionality
python test/test_todo_write.py

# Test smart cropping
python test/test_crop_message.py

# Test history compression  
python test/test_history_compress.py
```

## 🎯 Architecture Philosophy

**Think → Act → Validate**

1. **Think**: AI analyzes requests and creates structured plans via TodoWrite
2. **Act**: Execute tasks systematically with tool calls
3. **Validate**: Require user confirmation for risky operations

The TodoWrite tool enhances this flow by providing transparent task organization, progress tracking, and completion validation - ensuring complex workflows are handled systematically and reliably.

## Quick Start

1. Clone the repository
2. Install dependencies
3. Run the agent with TodoWrite enabled
4. Watch as complex requests are automatically organized into manageable task lists

The system intelligently decides when to use structured task management, making it seamless for both simple queries and complex multi-step workflows.
