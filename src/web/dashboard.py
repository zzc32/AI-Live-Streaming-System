"""
Web Dashboard Module
Provides web interface for controlling the streaming system
"""

from flask import Blueprint, render_template, jsonify

# Create blueprint for web dashboard
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@dashboard_bp.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify({
        "status": "running",
        "version": "1.0.0",
        "features": [
            "AI Digital Human Avatars",
            "Multi-platform Streaming", 
            "Real-time Chat Integration",
            "Content Automation"
        ]
    })