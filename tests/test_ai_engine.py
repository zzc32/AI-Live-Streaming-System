"""
Tests for AI Engine module
"""

import unittest
from unittest.mock import patch, MagicMock
import os

class TestAIEngine(unittest.TestCase):
    """Test cases for AI Engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock environment variables
        os.environ['OPENAI_API_KEY'] = 'test-key'
        
    @patch('src.ai_engine.core.openai')
    @patch('src.ai_engine.core.pipeline')
    def test_ai_engine_initialization(self, mock_pipeline, mock_openai):
        """Test AI engine initialization"""
        from src.ai_engine.core import AIEngine
        
        # Mock the pipeline
        mock_pipeline.return_value = MagicMock()
        
        # Initialize AI engine
        ai_engine = AIEngine()
        ai_engine.initialize()
        
        # Check if initialization succeeded
        self.assertTrue(ai_engine.is_initialized)
        self.assertIsNotNone(ai_engine.text_generator)
        
    @patch('src.ai_engine.core.openai.ChatCompletion.create')
    def test_generate_response_with_openai(self, mock_openai):
        """Test response generation with OpenAI"""
        from src.ai_engine.core import AIEngine
        
        # Mock OpenAI response
        mock_openai.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Test AI response'
                    }
                }
            ]
        }
        
        ai_engine = AIEngine()
        ai_engine.is_initialized = True
        
        response = ai_engine.generate_response("Hello")
        
        self.assertEqual(response, "Test AI response")
        mock_openai.assert_called_once()
        
    def test_generate_response_without_initialization(self):
        """Test response generation when AI engine is not initialized"""
        from src.ai_engine.core import AIEngine
        
        ai_engine = AIEngine()
        ai_engine.is_initialized = False
        
        response = ai_engine.generate_response("Hello")
        
        self.assertEqual(response, "AI system is not ready. Please wait...")

if __name__ == '__main__':
    unittest.main()