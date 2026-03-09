"""
Helper Functions Module
Common utility functions
"""

import os
import logging
from typing import Dict, Any

def validate_environment() -> bool:
    """Validate that all required environment variables are set"""
    required_vars = [
        'SECRET_KEY',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logging.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def format_stream_url(platform: str, stream_key: str) -> str:
    """Format RTMP URL for streaming platform"""
    platforms = {
        'youtube': 'rtmp://a.rtmp.youtube.com/live2',
        'twitch': 'rtmp://live.twitch.tv/app',
        'facebook': 'rtmp://live-api-s.facebook.com:80/rtmp'
    }
    
    base_url = platforms.get(platform, '')
    if base_url and stream_key:
        return f"{base_url}/{stream_key}"
    
    return ""

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace unsafe characters
    unsafe_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    return filename[:255]  # Limit filename length