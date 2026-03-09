#!/usr/bin/env python3
"""
AI Live Streaming System - Main Application
Advanced AI-powered digital human live streaming system
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

class AIStreamingSystem:
    """Main AI streaming system class"""
    
    def __init__(self):
        self.is_streaming = False
        self.current_stream = None
        self.ai_engine = None
        self.streaming_controller = None
        
    def initialize_ai_engine(self):
        """Initialize AI components"""
        logger.info("Initializing AI Engine...")
        # AI engine initialization will be implemented in ai_engine module
        
    def initialize_streaming(self):
        """Initialize streaming components"""
        logger.info("Initializing Streaming Controller...")
        # Streaming controller initialization will be implemented in streaming module
        
    def start_stream(self, platform="youtube"):
        """Start live streaming"""
        if self.is_streaming:
            return {"status": "error", "message": "Stream is already running"}
        
        logger.info(f"Starting stream on {platform}")
        self.is_streaming = True
        self.current_stream = platform
        
        # Start AI processing
        self.initialize_ai_engine()
        
        # Start streaming
        self.initialize_streaming()
        
        return {"status": "success", "message": f"Stream started on {platform}"}
        
    def stop_stream(self):
        """Stop live streaming"""
        if not self.is_streaming:
            return {"status": "error", "message": "No active stream"}
        
        logger.info("Stopping stream")
        self.is_streaming = False
        self.current_stream = None
        
        return {"status": "success", "message": "Stream stopped"}
        
    def process_chat_message(self, message):
        """Process incoming chat messages"""
        if not self.is_streaming:
            return {"status": "error", "message": "Stream is not active"}
        
        logger.info(f"Processing chat message: {message}")
        
        # AI response generation will be implemented in ai_engine module
        response = f"AI Response to: {message}"
        
        return {"status": "success", "response": response}

# Global instance
streaming_system = AIStreamingSystem()

# Web Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/stream/start', methods=['POST'])
def start_stream_api():
    """API endpoint to start streaming"""
    data = request.get_json()
    platform = data.get('platform', 'youtube')
    
    result = streaming_system.start_stream(platform)
    socketio.emit('stream_status', {"streaming": streaming_system.is_streaming})
    
    return jsonify(result)

@app.route('/api/stream/stop', methods=['POST'])
def stop_stream_api():
    """API endpoint to stop streaming"""
    result = streaming_system.stop_stream()
    socketio.emit('stream_status', {"streaming": streaming_system.is_streaming})
    
    return jsonify(result)

@app.route('/api/chat/send', methods=['POST'])
def send_chat_message():
    """API endpoint to send chat messages"""
    data = request.get_json()
    message = data.get('message', '')
    
    result = streaming_system.process_chat_message(message)
    socketio.emit('chat_response', result)
    
    return jsonify(result)

@app.route('/api/status')
def get_status():
    """API endpoint to get system status"""
    return jsonify({
        "streaming": streaming_system.is_streaming,
        "current_stream": streaming_system.current_stream,
        "status": "running"
    })

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info("Client connected")
    socketio.emit('stream_status', {"streaming": streaming_system.is_streaming})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected")

if __name__ == '__main__':
    logger.info("Starting AI Live Streaming System...")
    
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Run the application
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )
