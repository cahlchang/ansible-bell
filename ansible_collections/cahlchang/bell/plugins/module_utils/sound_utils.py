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
import configparser
import pathlib

def load_ansible_cfg_settings():
    """Load sound settings from ansible.cfg file."""
    sound_settings = {
        'success_sound': None,
        'failure_sound': None,
        'volume': 1.0
    }
    
    # Try to locate ansible.cfg
    possible_paths = [
        os.path.join(os.getcwd(), 'ansible.cfg'),
        os.path.join(os.path.expanduser('~'), '.ansible.cfg'),
        '/etc/ansible/ansible.cfg'
    ]
    
    for cfg_path in possible_paths:
        if os.path.exists(cfg_path):
            try:
                config = configparser.ConfigParser()
                config.read(cfg_path)
                
                if 'callback_bell' in config:
                    if 'success_sound' in config['callback_bell']:
                        path = config['callback_bell']['success_sound']
                        if os.path.exists(path):
                            sound_settings['success_sound'] = path
                    
                    if 'failure_sound' in config['callback_bell']:
                        path = config['callback_bell']['failure_sound']
                        if os.path.exists(path):
                            sound_settings['failure_sound'] = path
                    
                    if 'volume' in config['callback_bell']:
                        try:
                            sound_settings['volume'] = float(config['callback_bell']['volume'])
                        except (ValueError, TypeError):
                            pass  # Use default if value can't be converted to float
                
                break  # Stop after first ansible.cfg found
            except Exception:
                pass  # Silently ignore parsing errors
    
    return sound_settings


def get_default_sound_path(type='success'):
    """Return the path to the default sound file.
    
    Args:
        type: Type of sound ('success' or 'failure')
    """
    # First check if there's a setting in ansible.cfg
    cfg_settings = load_ansible_cfg_settings()
    if type == 'failure' and cfg_settings['failure_sound']:
        return cfg_settings['failure_sound']
    elif type == 'success' and cfg_settings['success_sound']:
        return cfg_settings['success_sound']
    
    # Try to find the default sounds in the sample_sound directory
    # relative to the collection path
    collection_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    sample_sound_dir = os.path.join(collection_path, '..', '..', 'sample_sound')
    
    if os.path.exists(sample_sound_dir):
        if type == 'failure':
            failure_path = os.path.join(sample_sound_dir, 'failure_sound.wav')
            if os.path.exists(failure_path):
                return failure_path
        else:  # success or any other value
            success_path = os.path.join(sample_sound_dir, 'success_sound.wav')
            if os.path.exists(success_path):
                return success_path
    
    # Fallback to temp directory
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, "ansible_bell_default.wav")



def create_default_sound(type='success'):
    """Create a default beep sound file and return its path.
    
    Args:
        type: Type of sound ('success' or 'failure')
    """
    try:
        import wave
        import struct
        import math
        
        # First check if we can use an existing default sound
        sound_path = get_default_sound_path(type)
        if os.path.exists(sound_path):
            return sound_path
            
        # If not, create a new one
        sound_path = os.path.join(tempfile.gettempdir(), "ansible_bell_default.wav")
        
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

def get_volume_from_cfg():
    """Get volume setting from ansible.cfg if available."""
    cfg_settings = load_ansible_cfg_settings()
    return cfg_settings['volume']
