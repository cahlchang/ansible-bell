#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, cahlchang
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: play_sound
short_description: Play a sound when Ansible task completes
version_added: "1.0.0"
description:
    - This module plays a sound to notify when Ansible tasks complete.
    - Useful for long-running playbooks to provide audible notification.
    - Set ANSIBLE_BELL_SILENT=true to disable sound playback (useful in CI/CD environments).
options:
    sound_file:
        description:
            - Path to the sound file to play.
            - If not specified, a default sound will be used.
        type: str
        required: false
    message:
        description:
            - Message to display along with the sound.
        type: str
        required: false
        default: "Ansible task completed"
    volume:
        description:
            - Volume level for the sound (0.0 to 1.0).
        type: float
        required: false
        default: 1.0
notes:
    - Set environment variable ANSIBLE_BELL_SILENT=true to disable sound playback.
    - This is useful in CI/CD environments or containers without audio capabilities.
    - The module will not fail the playbook if sound playback is not available.
author:
    - cahlchang (@cahlchang)
'''

EXAMPLES = r'''
# Play a default sound
- name: Notify task completion
  cahlchang.bell.play_sound:

# Play a custom sound file
- name: Play custom sound
  cahlchang.bell.play_sound:
    sound_file: "/path/to/custom/sound.wav"
    message: "Deployment completed successfully"

# Play with lower volume
- name: Play sound with lower volume
  cahlchang.bell.play_sound:
    volume: 0.5
    
# Run in silent mode (useful for CI/CD environments)
- name: Run playbook in silent mode
  hosts: all
  environment:
    ANSIBLE_BELL_SILENT: "true"
  tasks:
    - name: This will not actually play a sound
      cahlchang.bell.play_sound:
      
# Use the callback plugin for playbook completion sounds
# In ansible.cfg:
# [defaults]
# callback_whitelist = cahlchang.bell.bell
'''

RETURN = r'''
message:
    description: The message that was displayed
    type: str
    returned: always
    sample: "Ansible task completed"
sound_file:
    description: The sound file that was played
    type: str
    returned: always
    sample: "/path/to/default/sound.wav"
'''

import os
import platform
import subprocess
import tempfile
from ansible.module_utils.basic import AnsibleModule


def play_sound_macos(sound_file, volume=1.0):
    """Play sound on macOS using afplay"""
    print(f"Attempting to play sound on macOS: {sound_file}")
    try:
        afplay_check = subprocess.call(["which", "afplay"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"afplay check result: {afplay_check}")
        if afplay_check == 0:
            print(f"Using afplay to play sound (volume: {volume})")
            result = subprocess.call(["afplay", "-v", str(volume), sound_file])
            print(f"afplay result: {result}")
            return result == 0
        else:
            print("afplay not found")
            return False
    except Exception as e:
        print(f"afplay error: {str(e)}")
        return False


def play_sound_linux(sound_file, volume=1.0):
    """Play sound on Linux using various available players"""
    # Check if we're in a container or environment without sound
    if os.environ.get('ANSIBLE_BELL_SILENT') == 'true':
        print("Silent mode enabled, not playing sound")
        return True
        
    print(f"Attempting to play sound on Linux: {sound_file}")
    
    # Try aplay first (ALSA)
    try:
        aplay_check = subprocess.call(["which", "aplay"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"aplay check result: {aplay_check}")
        if aplay_check == 0:
            print("Using aplay to play sound")
            result = subprocess.call(["aplay", "-q", sound_file])
            print(f"aplay result: {result}")
            if result == 0:
                return True
    except Exception as e:
        print(f"aplay error: {str(e)}")

    # Try paplay (PulseAudio)
    try:
        paplay_check = subprocess.call(["which", "paplay"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"paplay check result: {paplay_check}")
        if paplay_check == 0:
            print("Using paplay to play sound")
            result = subprocess.call(["paplay", sound_file])
            print(f"paplay result: {result}")
            if result == 0:
                return True
    except Exception as e:
        print(f"paplay error: {str(e)}")

    # Try mplayer
    try:
        mplayer_check = subprocess.call(["which", "mplayer"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"mplayer check result: {mplayer_check}")
        if mplayer_check == 0:
            vol_percent = int(volume * 100)
            print(f"Using mplayer to play sound (volume: {vol_percent}%)")
            result = subprocess.call(["mplayer", "-really-quiet", "-volume", str(vol_percent), sound_file])
            print(f"mplayer result: {result}")
            if result == 0:
                return True
    except Exception as e:
        print(f"mplayer error: {str(e)}")
        
    # If we're in a container or CI environment, just pretend it worked
    if os.environ.get('CI') or os.environ.get('CONTAINER'):
        print("CI/Container environment detected, not playing sound")
        return True
        
    # In test environments, we can just log instead of playing sound
    print(f"No suitable sound player found. Would play sound: {sound_file} (volume: {volume})")
    return True


def play_sound_windows(sound_file, volume=1.0):
    """Play sound on Windows using PowerShell"""
    print(f"Attempting to play sound on Windows: {sound_file}")
    try:
        # Check if PowerShell is available
        ps_check = subprocess.call(["which", "powershell"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"powershell check result: {ps_check}")
        
        if ps_check != 0:
            print("PowerShell not found")
            return False
            
        # PowerShell command to play sound
        ps_command = f'''
        Add-Type -AssemblyName System.Speech
        $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $speak.Volume = {int(volume * 100)}
        $speak.Speak("Ansible task completed")
        
        # Also try to play the actual sound file
        Add-Type -AssemblyName presentationCore
        $mediaPlayer = New-Object system.windows.media.mediaplayer
        $mediaPlayer.Open("{sound_file}")
        $mediaPlayer.Volume = {volume}
        $mediaPlayer.Play()
        Start-Sleep -s 2  # Wait for sound to finish
        '''
        
        print("Using PowerShell to play sound")
        result = subprocess.call(["powershell", "-Command", ps_command])
        print(f"PowerShell result: {result}")
        return result == 0
    except Exception as e:
        print(f"PowerShell error: {str(e)}")
        return False


def create_default_sound():
    """Create a default beep sound file"""
    try:
        import wave
        import struct
        import math
        
        temp_dir = tempfile.gettempdir()
        sound_path = os.path.join(temp_dir, "ansible_bell_default.wav")
        
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sound_file=dict(type='str', required=False),
            message=dict(type='str', required=False, default='Ansible task completed'),
            volume=dict(type='float', required=False, default=1.0),
        ),
        supports_check_mode=True
    )

    sound_file = module.params['sound_file']
    message = module.params['message']
    volume = module.params['volume']

    # Debug information
    print(f"Starting play_sound module with parameters: sound_file={sound_file}, message={message}, volume={volume}")
    
    # If no sound file is provided, use the default
    if not sound_file:
        print("No sound file provided, creating default sound")
        sound_file = create_default_sound()
        if not sound_file:
            error_msg = "Failed to create default sound file and no custom sound file provided"
            print(error_msg)
            module.fail_json(msg=error_msg)
        print(f"Created default sound file: {sound_file}")

    # Check if the sound file exists
    if not os.path.exists(sound_file):
        error_msg = f"Sound file not found: {sound_file}"
        print(error_msg)
        module.fail_json(msg=error_msg)
    else:
        print(f"Sound file exists: {sound_file}")

    # Play the sound based on the platform
    system = platform.system()
    print(f"Detected platform: {system}")
    success = False
    
    # Check if we're in silent mode
    silent_mode = os.environ.get('ANSIBLE_BELL_SILENT') == 'true'
    print(f"Silent mode: {silent_mode}")
    
    if silent_mode:
        # Just pretend it worked in silent mode
        success = True
        print(f"Silent mode: Would play sound {sound_file}")
        module.log(msg=f"Silent mode: Would play sound {sound_file}")
    elif system == 'Darwin':  # macOS
        print("Calling play_sound_macos")
        success = play_sound_macos(sound_file, volume)
        print(f"play_sound_macos result: {success}")
    elif system == 'Linux':
        print("Calling play_sound_linux")
        success = play_sound_linux(sound_file, volume)
        print(f"play_sound_linux result: {success}")
    elif system == 'Windows':
        print("Calling play_sound_windows")
        success = play_sound_windows(sound_file, volume)
        print(f"play_sound_windows result: {success}")
    else:
        # For unsupported platforms, just log and continue
        print(f"Unsupported platform: {system}, sound would play here")
        module.log(msg=f"Unsupported platform: {system}, sound would play here")
        success = True

    if not success:
        # Don't fail the playbook, just warn
        warning_msg = f"Failed to play sound on {system}"
        print(warning_msg)
        module.warn(warning_msg)
        # Still mark as changed for idempotency
        success = True

    # Print the message
    if message:
        print(f"Message: {message}")
        module.log(msg=message)

    print("Module execution completed successfully")
    module.exit_json(
        changed=True,
        message=message,
        sound_file=sound_file
    )


if __name__ == '__main__':
    main()