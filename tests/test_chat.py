from backend.chat import chat_response

def test_chat_response():
    # Test basic chat functionality
    message = "Hello"
    history = []
    response = chat_response(message, history)
    
    assert isinstance(response, str)
    assert len(response) > 0
    assert "What brings you to our AI agency today?" in response 