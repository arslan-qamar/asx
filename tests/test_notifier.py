import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Notifier.notifier import telegram_bot_sendtext


class TestNotifier(unittest.TestCase):
    
    @patch.dict(os.environ, {'bot_token': 'test_token', 'bot_chatid': 'test_chat_id'})
    @patch('Notifier.notifier.telegram.Bot')
    def test_telegram_bot_sendtext_success(self, mock_bot_class):
        """Test that telegram_bot_sendtext sends message successfully"""
        # Mock the bot instance and its send_message method
        mock_bot = Mock()
        mock_response = Mock()
        mock_bot.send_message.return_value = mock_response
        mock_bot_class.return_value = mock_bot
        
        # Test message
        test_message = "Test notification message"
        
        # Call the function
        result = telegram_bot_sendtext(test_message)
        
        # Verify bot was created with correct token
        mock_bot_class.assert_called_once_with(token='test_token')
        
        # Verify send_message was called with correct parameters
        import telegram
        mock_bot.send_message.assert_called_once_with(
            chat_id='test_chat_id',
            text=test_message,
            parse_mode=telegram.constants.ParseMode.HTML
        )
        
        # Verify result
        self.assertEqual(result, mock_response)
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('Notifier.notifier.telegram.Bot')
    def test_telegram_bot_sendtext_missing_env_vars(self, mock_bot_class):
        """Test that telegram_bot_sendtext handles missing environment variables"""
        # Mock the bot instance
        mock_bot = Mock()
        mock_bot_class.return_value = mock_bot
        
        test_message = "Test message"
        
        # Call the function - it should still work but with None values
        result = telegram_bot_sendtext(test_message)
        
        # Verify bot was created with None token
        mock_bot_class.assert_called_once_with(token=None)
        
        # Verify send_message was called with None chat_id
        import telegram
        mock_bot.send_message.assert_called_once_with(
            chat_id=None,
            text=test_message,
            parse_mode=telegram.constants.ParseMode.HTML
        )
    
    @patch.dict(os.environ, {'bot_token': 'test_token', 'bot_chatid': 'test_chat_id'})
    @patch('Notifier.notifier.telegram.Bot')
    def test_telegram_bot_sendtext_with_html_message(self, mock_bot_class):
        """Test that telegram_bot_sendtext handles HTML formatted messages"""
        mock_bot = Mock()
        mock_response = Mock()
        mock_bot.send_message.return_value = mock_response
        mock_bot_class.return_value = mock_bot
        
        # Test HTML message
        html_message = "<b>Bold text</b> and <i>italic text</i>"
        
        # Call the function
        result = telegram_bot_sendtext(html_message)
        
        # Verify HTML parse mode is used
        import telegram
        mock_bot.send_message.assert_called_once_with(
            chat_id='test_chat_id',
            text=html_message,
            parse_mode=telegram.constants.ParseMode.HTML
        )
        
        self.assertEqual(result, mock_response)


if __name__ == '__main__':
    unittest.main()