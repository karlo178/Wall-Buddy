import pytest
from unittest.mock import Mock, patch, call
import Azure_STT_TTS_API
from windows import TaskManager

# Import the necessary modules from Azure_STT_TTS_API
from Azure_STT_TTS_API import speech_to_text, text_to_speech

@pytest.fixture
def task_manager():
    root = Mock()
    modern_gui = Mock()
    task_manager = TaskManager(root, modern_gui)    
    task_manager.check_queue()  # Start checking the queue
    return task_manager

@patch('Azure_STT_TTS_API.speech_to_text')
def test_handle_user_input_help(mock_speech_to_text, task_manager, mocker):
    mock_speech_to_text.return_value = "Hi, Buddy. Help."
    mocker.patch('Azure_STT_TTS_API.text_to_speech')

    # Preserve the original signature of take_user_input
    mocker.patch.object(TaskManager, 'take_user_input', autospec=True)

    # Simulate the 'get weather' branch
    task_manager.handle_user_input("Help.")

    TaskManager.take_user_input.assert_called_with(task_manager, "Now tell me, what should I do?")
    assert Azure_STT_TTS_API.text_to_speech.called

@patch('Azure_STT_TTS_API.speech_to_text')
def test_handle_user_input_invalid_command(mock_speech_to_text, task_manager, mocker):
    mock_speech_to_text.return_value = "Hi, Buddy. Invalid Command."
    mocker.patch('Azure_STT_TTS_API.text_to_speech')

    # Preserve the original signature of take_user_input
    mocker.patch.object(TaskManager, 'take_user_input', autospec=True)

    # Simulate the 'else' branch
    task_manager.handle_user_input("Invalid Command.")

    assert Azure_STT_TTS_API.text_to_speech.called

# Additional tests can be added based on the specific functionality of your code
