# Chapter 3: Real-Time Streaming Agent

[中文版本](./README_zh.md)

## What's New in Chapter 3

Chapter 3 enhances the ReAct agent from Chapter 2 with **real-time streaming capabilities** and improved configuration management:

### 🚀 Real-Time Streaming Output
- **Character-by-character display**: See AI responses as they're generated
- **Streaming tool calls**: Tool execution works seamlessly with streaming
- **Graceful degradation**: Auto-fallback to standard mode if streaming fails
- **Improved UX**: No more waiting for complete responses

### 🔧 Configuration Externalization  
- **Environment variables**: API keys and settings moved to `.env` file
- **Security improvement**: No hardcoded credentials in source code
- **Flexible deployment**: Easy configuration for different environments

## User Experience Comparison

**Chapter 2 (Standard Mode)**:
```
User: Help me list files
[3-5 second wait]
AI: I'll help you list files in the current directory...
```

**Chapter 3 (Streaming Mode)** ✨:
```
User: Help me list files  
AI: I'll help you list files in the current directory...
    [Text appears in real-time, no waiting]
```

## Technical Implementation

### Streaming API Client
[`APIClient`](src/core/api_client.py) now supports dual modes:

```python
# Standard mode (backward compatible)
def get_completion(self, request_params) -> Message

# Streaming mode (new)
def get_completion_stream(self, request_params) -> Generator[str, None, None]
```

### Enhanced Conversation Manager
[`Conversation`](src/core/conversation.py) streaming features:

```python
def print_streaming_content(self, content_chunk):
    """Display AI response chunks in real-time"""
    
def recursive_message_handling(self, message):
    """Enhanced to support streaming with tool calls"""
```

### Configuration Management
Environment variables in `.env`:
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=anthropic/claude-3.5-sonnet
```

## Streaming Benefits

- **Immediate feedback**: Users see progress instantly
- **Better perceived performance**: Feels faster even with same latency
- **Maintained functionality**: All Chapter 2 features work with streaming
- **Error resilience**: Automatic fallback ensures reliability

## Technical Details

### Stream Processing
```python
for chunk in stream:
    if chunk.choices[0].delta.content:
        content_chunk = chunk.choices[0].delta.content
        yield content_chunk  # Real-time display
```

### Tool Call Streaming
```python
# Build tool calls incrementally during streaming
if hasattr(chunk.choices[0].delta, 'tool_calls'):
    # Accumulate tool call data
    # Execute when complete
```

## Next Steps

→ **Chapter 4**: Add intelligent conversation history management and cost tracking for long-running sessions.
