#!/usr/bin/env python3
"""
Simple test script to verify streaming functionality
"""
import sys
import os
sys.path.append('src')

from core.api_client import APIClient

def test_streaming():
    """Test the streaming API functionality"""
    print("🧪 Testing streaming functionality...")
    
    try:
        client = APIClient()
        
        # Simple test request
        request_params = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in a friendly way"}
            ]
        }
        
        print("📡 Making streaming request...")
        print("📝 Streaming response:")
        print("🤖 ", end="", flush=True)
        
        # Test the streaming generator
        stream_gen = client.get_completion_stream(request_params)
        
        for chunk in stream_gen:
            if isinstance(chunk, str):
                print(chunk, end="", flush=True)
            else:
                print(f"\n✅ Received final message object with content length: {len(chunk.content) if chunk.content else 0}")
                break
        
        print("\n🎉 Streaming test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Streaming test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_streaming()
    sys.exit(0 if success else 1)
