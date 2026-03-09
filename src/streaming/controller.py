"""
Streaming Controller Module
Handles multi-platform streaming and RTMP server management
"""

import os
import logging
import subprocess
from typing import Dict, Any, List
import yaml

logger = logging.getLogger(__name__)

class StreamingController:
    """Manages streaming to multiple platforms"""
    
    def __init__(self):
        self.is_streaming = False
        self.current_platforms = []
        self.ffmpeg_process = None
        self.platform_config = {}
        
    def load_config(self, config_path: str = "config/platforms.yaml"):
        """Load streaming platform configurations"""
        try:
            with open(config_path, 'r') as f:
                self.platform_config = yaml.safe_load(f)
            logger.info("Streaming configuration loaded")
        except Exception as e:
            logger.error(f"Failed to load streaming config: {e}")
            self.platform_config = {}
    
    def start_stream(self, platforms: List[str] = None) -> Dict[str, Any]:
        """Start streaming to specified platforms"""
        if self.is_streaming:
            return {"status": "error", "message": "Stream is already running"}
        
        if not platforms:
            platforms = ["youtube", "twitch"]  # Default platforms
        
        try:
            # Validate platforms
            valid_platforms = []
            for platform in platforms:
                if (platform in self.platform_config and 
                    self.platform_config[platform].get('enabled', False)):
                    valid_platforms.append(platform)
            
            if not valid_platforms:
                return {"status": "error", "message": "No valid platforms configured"}
            
            # Start FFmpeg streaming process
            self._start_ffmpeg_stream(valid_platforms)
            
            self.is_streaming = True
            self.current_platforms = valid_platforms
            
            logger.info(f"Started streaming to: {', '.join(valid_platforms)}")
            return {
                "status": "success", 
                "message": f"Streaming started to {', '.join(valid_platforms)}",
                "platforms": valid_platforms
            }
            
        except Exception as e:
            logger.error(f"Failed to start stream: {e}")
            return {"status": "error", "message": f"Stream start failed: {e}"}
    
    def stop_stream(self) -> Dict[str, Any]:
        """Stop current streaming session"""
        if not self.is_streaming:
            return {"status": "error", "message": "No active stream"}
        
        try:
            # Stop FFmpeg process
            if self.ffmpeg_process:
                self.ffmpeg_process.terminate()
                self.ffmpeg_process.wait()
                self.ffmpeg_process = None
            
            self.is_streaming = False
            self.current_platforms = []
            
            logger.info("Streaming stopped")
            return {"status": "success", "message": "Streaming stopped"}
            
        except Exception as e:
            logger.error(f"Error stopping stream: {e}")
            return {"status": "error", "message": f"Stream stop failed: {e}"}
    
    def _start_ffmpeg_stream(self, platforms: List[str]):
        """Start FFmpeg streaming process for multiple platforms"""
        # This is a simplified implementation
        # In production, you'd use proper RTMP multiplexing
        
        ffmpeg_command = [
            "ffmpeg",
            "-f", "lavfi", "-i", "testsrc=size=1920x1080:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=1000",
            "-c:v", "libx264", "-preset", "veryfast", "-b:v", "3000k",
            "-maxrate", "3000k", "-bufsize", "6000k",
            "-pix_fmt", "yuv420p", "-g", "60",
            "-c:a", "aac", "-b:a", "128k",
            "-f", "flv"
        ]
        
        # Add RTMP URLs for each platform
        for platform in platforms:
            if platform in self.platform_config:
                config = self.platform_config[platform]
                rtmp_url = config.get('rtmp_url', '')
                stream_key = os.getenv(f'{platform.upper()}_STREAM_KEY', '')
                
                if rtmp_url and stream_key:
                    full_url = f"{rtmp_url}/{stream_key}"
                    ffmpeg_command.append(full_url)
        
        # Start FFmpeg process
        self.ffmpeg_process = subprocess.Popen(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    def get_stream_status(self) -> Dict[str, Any]:
        """Get current streaming status"""
        return {
            "is_streaming": self.is_streaming,
            "current_platforms": self.current_platforms,
            "ffmpeg_running": self.ffmpeg_process is not None
        }
