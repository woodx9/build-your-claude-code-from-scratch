import sys
import os
import traceback

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.history.history_manager import HistoryManager, Role, Crop_Direction


def create_mock_message(role: Role, content: str) -> dict:
    """Create a mock message dictionary compatible with crop_message function"""
    return {'role': role, 'content': content}


def setup_history_manager():
    """Setup a fresh HistoryManager instance for testing"""
    # Reset singleton instance to ensure clean state
    HistoryManager._instance = None
    HistoryManager._initialized = False
    return HistoryManager(model_max_tokens=100, compress_threshold=0.8)


def test_crop_insufficient_messages():
    """Test cropping when there are insufficient messages"""
    print("测试: 消息数量不足时的裁剪")
    
    manager = setup_history_manager()
    
    # Test with no messages
    result = manager.crop_message(Crop_Direction.TOP, 1)
    assert result == "Cannot crop: insufficient messages"
    
    # Test with only one message
    manager.add_message(create_mock_message(Role.SYSTEM, "System message"))
    result = manager.crop_message(Crop_Direction.TOP, 1)
    assert result == "Cannot crop: insufficient messages"
    
    print("✓ 通过: 消息数量不足时正确拒绝裁剪")


def test_crop_invalid_amount():
    """Test cropping with invalid crop amount"""
    print("\n测试: 无效裁剪数量")
    
    manager = setup_history_manager()
    
    # Add 4 messages - with crop_amount=2, check becomes 4 <= 2+2 = true, so invalid
    manager.add_message(create_mock_message(Role.SYSTEM, "System message"))
    manager.add_message(create_mock_message(Role.USER, "User message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Assistant message"))

    
    result = manager.crop_message(Crop_Direction.TOP, 2)
    assert result == "Cannot crop: invalid crop amount"
    
    print("✓ 通过: 无效裁剪数量时正确拒绝")


def test_crop_no_user_messages():
    """Test cropping when no user messages exist"""
    print("\n测试: 没有用户消息时的裁剪")
    
    manager = setup_history_manager()
    
    # Add 5 messages with no user messages to pass the count check
    manager.add_message(create_mock_message(Role.SYSTEM, "System message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Assistant message"))
    manager.add_message(create_mock_message(Role.TOOL, "Tool message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Another assistant message"))
    manager.add_message(create_mock_message(Role.TOOL, "Another tool message"))
    
    result = manager.crop_message(Crop_Direction.TOP, 1)
    assert result == "Cannot crop: no user messages found"
    
    print("✓ 通过: 没有用户消息时正确拒绝裁剪")


def test_crop_would_remove_latest_user_message():
    """Test cropping that would remove the latest user message"""
    print("\n测试: 尝试裁剪最新用户消息时的保护")
    
    manager = setup_history_manager()
    
    # Add 8 messages with user message in the middle
    manager.add_message(create_mock_message(Role.SYSTEM, "System message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Assistant message 1"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Assistant message 2"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Assistant message 3"))
    manager.add_message(create_mock_message(Role.USER, "Latest user message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Final assistant message"))
    manager.add_message(create_mock_message(Role.TOOL, "Tool message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Another assistant message"))
    
    # Try to crop 5 messages from top, which would remove the user message at index 4
    result = manager.crop_message(Crop_Direction.TOP, 5)
    assert result == "Cannot crop: can't crop the latest user message"
    
    print("✓ 通过: 正确保护最新用户消息不被裁剪")


def test_crop_top_success():
    """Test successful top cropping"""
    print("\n测试: 从顶部成功裁剪")
    
    manager = setup_history_manager()
    
    # Add 6 messages to have enough for cropping
    manager.add_message(create_mock_message(Role.SYSTEM, "System message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Old assistant message"))
    manager.add_message(create_mock_message(Role.TOOL, "Old tool message"))
    manager.add_message(create_mock_message(Role.USER, "User message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Recent assistant message"))
    manager.add_message(create_mock_message(Role.TOOL, "Recent tool message"))
    
    # Crop 2 messages from top
    result = manager.crop_message(Crop_Direction.TOP, 2)
    assert result == "Crop message successful"
    
    messages = manager.get_current_messages()
    
    # Should have 4 messages left (system + user + 2 recent messages)
    assert len(messages) == 5
    
    # Should preserve system messages
    system_messages = [msg for msg in messages if msg['role'] == Role.SYSTEM]
    assert len(system_messages) == 1
    assert system_messages[0]['content'] == "System message"
    
    # Should preserve user message and later messages
    assert messages[2]['content'] == "User message"
    assert messages[3]['content'] == "Recent assistant message"
    assert messages[4]['content'] == "Recent tool message"
    
    print("✓ 通过: 从顶部成功裁剪，保留系统消息和用户消息后的内容")


def test_crop_bottom_success():
    """Test successful bottom cropping"""
    print("\n测试: 从底部成功裁剪")
    
    manager = setup_history_manager()
    
    # Add multiple messages
    manager.add_message(create_mock_message(Role.SYSTEM, "System message"))
    manager.add_message(create_mock_message(Role.USER, "User message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Assistant message 1"))
    manager.add_message(create_mock_message(Role.TOOL, "Tool message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Assistant message 2"))
    
    # Crop 2 messages from bottom
    result = manager.crop_message(Crop_Direction.BOTTOM, 2)
    assert result == "Crop message successful"
    
    messages = manager.get_current_messages()
    
    # Should have 3 messages left
    assert len(messages) == 3
    
    # Should preserve user message (cannot be cropped)
    user_messages = [msg for msg in messages if msg['role'] == Role.USER]
    assert len(user_messages) == 1
    assert user_messages[0]['content'] == "User message"
    
    # Should preserve earlier messages
    assert messages[0]['content'] == "System message"
    assert messages[1]['content'] == "User message"
    assert messages[2]['content'] == "Assistant message 1"
    
    print("✓ 通过: 从底部成功裁剪，保护最新用户消息")


def test_crop_multiple_user_messages():
    """Test cropping with multiple user messages"""
    print("\n测试: 多个用户消息的裁剪")
    
    manager = setup_history_manager()
    
    # Add messages with multiple user messages
    manager.add_message(create_mock_message(Role.SYSTEM, "System message"))
    manager.add_message(create_mock_message(Role.USER, "First user message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "First assistant response"))
    manager.add_message(create_mock_message(Role.USER, "Second user message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Second assistant response"))
    manager.add_message(create_mock_message(Role.USER, "Latest user message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Latest assistant response"))
    
    # Crop from top - latest user is at index 5, so we can crop up to 5 messages
    result = manager.crop_message(Crop_Direction.TOP, 2)
    assert result == "Crop message successful"
    
    messages = manager.get_current_messages()
    
    # Should preserve system message and content after cropping
    assert messages[0]['role'] == Role.SYSTEM
    
    # Should preserve the latest user message
    user_messages = [msg for msg in messages if msg['role'] == Role.USER]
    latest_user = user_messages[-1]
    assert latest_user['content'] == "Latest user message"
    
    print("✓ 通过: 多用户消息场景下正确裁剪")


def test_crop_edge_cases():
    """Test edge cases for cropping"""
    print("\n测试: 边界情况")
    
    manager = setup_history_manager()
    
    # Add minimum viable messages for cropping (5 messages)
    manager.add_message(create_mock_message(Role.SYSTEM, "System message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Assistant message"))
    manager.add_message(create_mock_message(Role.USER, "User message"))
    manager.add_message(create_mock_message(Role.ASSISTANT, "Final assistant message"))
    manager.add_message(create_mock_message(Role.TOOL, "Tool message"))
    
    # Test maximum valid crop amount from top
    result = manager.crop_message(Crop_Direction.TOP, 1)
    assert result == "Crop message successful"
    
    messages = manager.get_current_messages()
    assert len(messages) == 5  # system + user + 2 remaining messages
    
    print("✓ 通过: 边界情况处理正确")


def run_all_tests():
    """运行所有测试"""
    print("开始运行 crop_message 函数测试...\n")
    
    try:
        test_crop_insufficient_messages()
        test_crop_invalid_amount()
        test_crop_no_user_messages()
        test_crop_would_remove_latest_user_message()
        test_crop_top_success()
        test_crop_bottom_success()
        test_crop_multiple_user_messages()
        test_crop_edge_cases()
        
        print("\n🎉 所有测试通过!")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
