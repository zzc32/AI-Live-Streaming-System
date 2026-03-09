#!/bin/bash

# AI Live Streaming System Setup Script
# This script sets up the environment and installs dependencies

echo "🤖 Setting up AI Live Streaming System..."

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is not installed. Please install FFmpeg for streaming capabilities."
    echo "Ubuntu/Debian: sudo apt install ffmpeg"
    echo "macOS: brew install ffmpeg"
    echo "Windows: Download from https://ffmpeg.org/"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p models
mkdir -p animations

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Copying environment configuration..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys and settings"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the system:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "🌐 Then open http://localhost:5000 in your browser"