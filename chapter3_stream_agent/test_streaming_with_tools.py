#!/usr/bin/env python3
"""
Test streaming functionality with tool calls
"""
import sys
import os

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from core.api_client import APIClient
from tools.tool_manager import ToolManager

def test_streaming_with_tools():
    """Test streaming with tool calls"""
    print("🧪 Testing streaming functionality with tools...")
    
    try:
        client = APIClient()
        tool_manager = ToolManager()
        
        # Test request that should trigger a tool call
        request_params = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Please list the files in the current directory"}
            ],
            "tools": tool_manager.get_tools_description()
        }
        
        print("📡 Making streaming request with tools...")
        print("📝 Streaming response:")
        print("🤖 ", end="", flush=True)
        
        stream_gen = client.get_completion_stream(request_params)
        full_content = ""
        message_obj = None
        
        for chunk in stream_gen:
            if isinstance(chunk, str):
                print(chunk, end="", flush=True)
                full_content += chunk
            else:
                message_obj = chunk
                print(f"\n✅ Received final message object")
                print(f"   Content length: {len(chunk.content) if chunk.content else 0}")
                print(f"   Has tool_calls: {hasattr(chunk, 'tool_calls') and chunk.tool_calls is not None}")
                if hasattr(chunk, 'tool_calls') and chunk.tool_calls:
                    print(f"   Number of tool calls: {len(chunk.tool_calls)}")
                    for i, tc in enumerate(chunk.tool_calls):
                        print(f"   Tool call {i+1}: {tc.function.name}")
                break
        
        print(f"\n📊 Results:")
        print(f"   Streamed content: '{full_content.strip()}'")
        print(f"   Tool calls detected: {message_obj and hasattr(message_obj, 'tool_calls') and message_obj.tool_calls is not None}")
        
        print("🎉 Tool streaming test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Tool streaming test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_streaming_with_tools()
    sys.exit(0 if success else 1)
