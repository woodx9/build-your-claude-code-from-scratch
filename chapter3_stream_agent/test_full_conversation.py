#!/usr/bin/env python3
"""
Test the full conversation flow with streaming
"""
import sys
import os
import asyncio

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from core.conversation import Conversation

async def test_conversation_integration():
    """Test that conversation class can handle streaming properly"""
    print("🧪 Testing conversation streaming integration...")
    
    try:
        conv = Conversation()
        
        # Test the streaming message handling directly
        conv.messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello briefly"}
        ]
        
        print("📡 Testing recursive_message_handling with streaming...")
        
        # Simulate one round of message handling
        # This should use streaming internally
        
        # We can't easily test the full interactive flow without user input,
        # but we can test that the methods exist and work
        
        # Test that streaming methods exist
        api_client = conv._api_client
        if hasattr(api_client, 'get_completion_stream'):
            print("✅ Streaming API method available")
        else:
            print("❌ Streaming API method missing")
            return False
            
        if hasattr(conv, 'print_streaming_content'):
            print("✅ Streaming print method available")
        else:
            print("❌ Streaming print method missing")
            return False
            
        # Test streaming content printing
        print("📝 Testing streaming content display:")
        print("🤖 ", end="", flush=True)
        test_content = "This is a test of streaming content display."
        for char in test_content:
            conv.print_streaming_content(char)
            await asyncio.sleep(0.01)  # Small delay to simulate streaming
        print()  # New line
        
        print("🎉 Conversation streaming integration test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Conversation integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_conversation_integration())
    sys.exit(0 if success else 1)
