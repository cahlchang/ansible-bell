#!/bin/bash

# Setup script for Ansible Bell collection

set -e

echo "Setting up dependencies for Ansible Bell collection..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux system"
    
    # Check for package managers
    if command -v apt-get &> /dev/null; then
        echo "Installing dependencies with apt..."
        sudo apt-get update
        sudo apt-get install -y alsa-utils pulseaudio-utils mplayer
    elif command -v yum &> /dev/null; then
        echo "Installing dependencies with yum..."
        sudo yum install -y alsa-utils pulseaudio-utils mplayer
    elif command -v dnf &> /dev/null; then
        echo "Installing dependencies with dnf..."
        sudo dnf install -y alsa-utils pulseaudio-utils mplayer
    elif command -v pacman &> /dev/null; then
        echo "Installing dependencies with pacman..."
        sudo pacman -S --noconfirm alsa-utils pulseaudio mplayer
    else
        echo "WARNING: Could not detect package manager. Please install aplay, paplay, or mplayer manually."
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS system"
    echo "No additional dependencies needed. macOS includes afplay by default."
    
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "Detected Windows system"
    echo "No additional dependencies needed. PowerShell will be used for sound playback."
    
else
    echo "WARNING: Unsupported operating system: $OSTYPE"
    echo "Please ensure you have appropriate sound playback utilities installed."
fi

echo "Setup complete!"
echo "You can now build and install the collection with ./build.sh"