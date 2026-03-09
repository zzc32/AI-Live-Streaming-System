"""
Tests for Streaming Controller module
"""

import unittest
from unittest.mock import patch, MagicMock
import os

class TestStreamingController(unittest.TestCase):
    """Test cases for Streaming Controller"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock environment variables
        os.environ['YOUTUBE_STREAM_KEY'] = 'test-youtube-key'
        os.environ['TWITCH_STREAM_KEY'] = 'test-twitch-key'
        
    @patch('src.streaming.controller.subprocess.Popen')
    @patch('src.streaming.controller.yaml.safe_load')
    def test_start_stream_success(self, mock_yaml_load, mock_popen):
        """Test successful stream start"""
        from src.streaming.controller import StreamingController
        
        # Mock YAML configuration
        mock_yaml_load.return_value = {
            'youtube': {'enabled': True, 'rtmp_url': 'rtmp://test.youtube.com'},
            'twitch': {'enabled': True, 'rtmp_url': 'rtmp://test.twitch.tv'}
        }
        
        # Mock subprocess
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        controller = StreamingController()
        controller.load_config()
        
        result = controller.start_stream(['youtube', 'twitch'])
        
        self.assertEqual(result['status'], 'success')
        self.assertTrue(controller.is_streaming)
        self.assertEqual(controller.current_platforms, ['youtube', 'twitch'])
        
    @patch('src.streaming.controller.yaml.safe_load')
    def test_start_stream_no_valid_platforms(self, mock_yaml_load):
        """Test stream start with no valid platforms"""
        from src.streaming.controller import StreamingController
        
        # Mock YAML configuration with no enabled platforms
        mock_yaml_load.return_value = {
            'youtube': {'enabled': False},
            'twitch': {'enabled': False}
        }
        
        controller = StreamingController()
        controller.load_config()
        
        result = controller.start_stream(['youtube', 'twitch'])
        
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['message'], 'No valid platforms configured')
        self.assertFalse(controller.is_streaming)
        
    def test_stop_stream_when_not_streaming(self):
        """Test stopping stream when no stream is active"""
        from src.streaming.controller import StreamingController
        
        controller = StreamingController()
        controller.is_streaming = False
        
        result = controller.stop_stream()
        
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['message'], 'No active stream')
        
    @patch('src.streaming.controller.subprocess.Popen')
    @patch('src.streaming.controller.yaml.safe_load')
    def test_get_stream_status(self, mock_yaml_load, mock_popen):
        """Test getting stream status"""
        from src.streaming.controller import StreamingController
        
        # Mock configuration and process
        mock_yaml_load.return_value = {'youtube': {'enabled': True}}
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        controller = StreamingController()
        controller.load_config()
        controller.start_stream(['youtube'])
        
        status = controller.get_stream_status()
        
        self.assertTrue(status['is_streaming'])
        self.assertEqual(status['current_platforms'], ['youtube'])
        self.assertTrue(status['ffmpeg_running'])

if __name__ == '__main__':
    unittest.main()