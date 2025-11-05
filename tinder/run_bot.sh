#!/bin/bash

# Install Xvfb if not already installed
if ! command -v Xvfb &> /dev/null; then
    echo "Installing Xvfb..."
    sudo apt-get update && sudo apt-get install -y xvfb
fi

# Start Xvfb on display :99
Xvfb :99 -screen 0 1920x1080x16 &
export DISPLAY=:99

# Install Chrome if not already installed
if ! command -v google-chrome &> /dev/null; then
    echo "Installing Google Chrome..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install -y ./google-chrome-stable_current_amd64.deb
    rm google-chrome-stable_current_amd64.deb
fi

# Make sure we're in the script's directory
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

# Install required Python packages
pip install -r requirements.txt

# Run the bot with manual login enabled
# You can modify the parameters as needed
python daily_swipe.py True 10 50.25% 4 False

# Kill Xvfb when done
killall Xvfb
