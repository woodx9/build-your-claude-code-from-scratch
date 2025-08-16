# Chapter 4: Intelligent History Management

[中文版本](./README_zh.md)

## What's New in Chapter 4

Chapter 4 extends the streaming agent with **intelligent conversation history management** and **comprehensive cost tracking**:

### 🧠 Auto History Compression
- **Smart compression**: Automatically manages context window usage
- **Token monitoring**: Real-time context usage percentage display  
- **Multi-session strategy**: Removes oldest complete conversations first
- **Single-session strategy**: Removes intermediate responses when needed
- **Preservation guarantee**: Always keeps system messages and recent context

### 💰 Cost Tracking System
- **Real-time monitoring**: Track API costs during conversations
- **Token-based calculation**: Accurate cost estimates based on actual usage
- **Model-specific pricing**: Supports different pricing tiers per model
- **Session summaries**: Cost breakdowns per conversation session

## History Compression Strategies

### Multi-Session Compression
When context approaches limits, remove entire conversation sessions:
```
[System Message] ← Always preserved
[Old Session 1] ← Removed first
[Old Session 2] ← Removed next  
[Recent Session] ← Always kept
[Current Session] ← Always kept
```

### Single-Session Compression  
Within current session, remove intermediate tool responses:
```
User: "Run command X"
Assistant: "I'll run that command"
[Tool Result] ← Can be removed
Assistant: "Command completed successfully"
User: "Now run command Y" ← Recent messages preserved
```

## Technical Implementation

### History Manager
[`HistoryManager`](src/core/history_manager.py) - Intelligent compression:

```python
def compress_history_if_needed(self, messages, max_tokens):
    """Auto-compress when approaching context limits"""
    
def multi_session_compression(self, messages):
    """Remove oldest complete conversation sessions"""
    
def single_session_compression(self, messages):  
    """Remove intermediate responses within current session"""
```

### Cost Tracker
[`CostTracker`](src/core/cost_tracker.py) - Monitor API expenses:

```python
def calculate_cost(self, input_tokens, output_tokens, model_name):
    """Calculate cost based on token usage and model pricing"""
    
def display_cost_info(self, session_cost, total_cost):
    """Show real-time cost information to user"""
```

## User Experience Enhancements

### Context Monitoring
```
💬 Context: 3,456/8,192 tokens (42%) 💰 Session: $0.023
```

### Auto-Compression Notifications
```
🧠 Context getting full (85%). Compressing history...
✅ Compressed 2 old sessions. Context: 2,100/8,192 tokens (26%)
```

### Cost Awareness
```
💰 API Cost Summary:
   This session: $0.045
   Total today: $0.156
   Model: Claude 3.5 Sonnet
```

## Configuration

Enhanced environment variables:
```env
# API Configuration (from Chapter 3)
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=anthropic/claude-3.5-sonnet

# History Management (new)
MAX_CONTEXT_TOKENS=8192
COMPRESSION_THRESHOLD=0.85

# Cost Tracking (new)  
ENABLE_COST_TRACKING=true
DAILY_COST_LIMIT=10.00
```

## Benefits

- **Cost control**: Avoid unexpected API charges with real-time monitoring
- **Performance**: Maintain fast responses by managing context size
- **Longevity**: Support extended conversations without manual intervention
- **Transparency**: Clear visibility into resource usage and costs

## Next Steps

→ **Chapter 5**: Add smart context cropping tools for fine-grained conversation management control.
