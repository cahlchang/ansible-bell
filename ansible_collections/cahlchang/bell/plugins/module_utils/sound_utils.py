#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, cahlchang
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Utility functions for sound playback in Ansible modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import platform
import subprocess
import tempfile


def get_default_sound_path():
    """Return the path to the default sound file."""
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, "ansible_bell_default.wav")


def create_default_sound():
    """Create a default beep sound file and return its path."""
    try:
        import wave
        import struct
        import math
        
        sound_path = get_default_sound_path()
        
        # Create a simple beep sound
        sample_rate = 44100
        duration = 0.5  # seconds
        frequency = 440  # Hz (A4 note)
        
        # Create the WAV file
        with wave.open(sound_path, 'w') as wav_file:
            wav_file.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))
            
            # Generate samples
            samples = []
            for i in range(int(duration * sample_rate)):
                sample = int(32767 * math.sin(2 * math.pi * frequency * i / sample_rate))
                samples.append(struct.pack('h', sample))
            
            wav_file.writeframes(b''.join(samples))
        
        return sound_path
    except Exception:
        return None


def detect_sound_players():
    """Detect available sound players on the system."""
    system = platform.system()
    players = []
    
    if system == 'Darwin':  # macOS
        if subprocess.call(['which', 'afplay'], stdout=subprocess.PIPE) == 0:
            players.append('afplay')
    
    elif system == 'Linux':
        # Check for ALSA
        if subprocess.call(['which', 'aplay'], stdout=subprocess.PIPE) == 0:
            players.append('aplay')
        
        # Check for PulseAudio
        if subprocess.call(['which', 'paplay'], stdout=subprocess.PIPE) == 0:
            players.append('paplay')
        
        # Check for mplayer
        if subprocess.call(['which', 'mplayer'], stdout=subprocess.PIPE) == 0:
            players.append('mplayer')
    
    elif system == 'Windows':
        # PowerShell is generally available on modern Windows
        if subprocess.call(['where', 'powershell'], stdout=subprocess.PIPE) == 0:
            players.append('powershell')
    
    return players