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


def get_sample_sounds_dir():
    """Return the path to the sample sounds directory."""
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the sample_sounds directory
    sample_sounds_dir = os.path.normpath(os.path.join(current_dir, '..', '..', 'sample_sounds'))
    return sample_sounds_dir


def get_default_sound_path(sound_type='success'):
    """Return the path to the default sound file.
    
    Args:
        sound_type: Either 'success' or 'failure'
    """
    # First try to get from sample_sounds directory
    sample_sounds_dir = get_sample_sounds_dir()
    if os.path.exists(sample_sounds_dir):
        sound_file = f"{sound_type}_sound.wav"
        sample_sound_path = os.path.join(sample_sounds_dir, sound_file)
        if os.path.exists(sample_sound_path):
            return sample_sound_path
    
    # Fallback to temp directory
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, "ansible_bell_default.wav")


def create_default_sound(sound_type='success'):
    """Create a default beep sound file and return its path.
    
    Args:
        sound_type: Either 'success' or 'failure'
    """
    # First check if we have sample sounds available
    sample_sound_path = get_default_sound_path(sound_type)
    if os.path.exists(sample_sound_path) and sample_sound_path.endswith('.wav'):
        return sample_sound_path
        
    # Otherwise create a default sound
    try:
        import wave
        import struct
        import math

        sound_path = os.path.join(tempfile.gettempdir(), "ansible_bell_default.wav")

        # Create a simple beep sound
        sample_rate = 44100
        duration = 0.5  # seconds
        frequency = 440  # Hz (A4 note)
        
        # Use different frequency for success vs failure
        if sound_type == 'failure':
            frequency = 330  # Lower tone for failure

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