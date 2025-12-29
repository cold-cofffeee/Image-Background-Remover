#!/bin/bash
# Start script for Linux/Mac

echo "Starting Image Background Remover..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if model exists
if [ ! -f "saved_models/u2net/u2net.pth" ]; then
    echo "WARNING: Model file not found!"
    echo "Attempting to download..."
    python download_model.py
    if [ $? -ne 0 ]; then
        echo "ERROR: Could not download model. Please run ./setup.sh"
        exit 1
    fi
fi

# Start the application
echo "Starting Flask application..."
python app.py
