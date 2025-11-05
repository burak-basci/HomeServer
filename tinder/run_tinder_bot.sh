#!/bin/bash

# Kill any existing Xvfb processes
pkill -f Xvfb

# Start Xvfb on display :99
Xvfb :99 -screen 0 1920x1080x16 &
export DISPLAY=:99

# Activate virtual environment
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run the Tinder bot
python3 daily_swipe.py True 10 50.25% 4 False

# Clean up
pkill -f Xvfb
