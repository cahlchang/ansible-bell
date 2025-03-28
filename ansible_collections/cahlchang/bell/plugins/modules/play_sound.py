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
    try:
        subprocess.call(["afplay", "-v", str(volume), sound_file])
        return True
    except Exception:
        return False


def play_sound_linux(sound_file, volume=1.0):
    """Play sound on Linux using various available players"""
    # Check if we're in a container or environment without sound
    if os.environ.get('ANSIBLE_BELL_SILENT') == 'true':
        return True
        
    # Try aplay first (ALSA)
    try:
        if subprocess.call(["which", "aplay"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
            subprocess.call(["aplay", "-q", sound_file])
            return True
    except Exception:
        pass

    # Try paplay (PulseAudio)
    try:
        if subprocess.call(["which", "paplay"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
            subprocess.call(["paplay", sound_file])
            return True
    except Exception:
        pass

    # Try mplayer
    try:
        if subprocess.call(["which", "mplayer"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
            vol_percent = int(volume * 100)
            subprocess.call(["mplayer", "-really-quiet", "-volume", str(vol_percent), sound_file])
            return True
    except Exception:
        pass
        
    # If we're in a container or CI environment, just pretend it worked
    if os.environ.get('CI') or os.environ.get('CONTAINER'):
        return True
        
    # In test environments, we can just log instead of playing sound
    print(f"Would play sound: {sound_file} (volume: {volume})")
    return True


def play_sound_windows(sound_file, volume=1.0):
    """Play sound on Windows using PowerShell"""
    try:
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
        
        subprocess.call(["powershell", "-Command", ps_command])
        return True
    except Exception:
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

    # If no sound file is provided, use the default
    if not sound_file:
        sound_file = create_default_sound()
        if not sound_file:
            module.fail_json(msg="Failed to create default sound file and no custom sound file provided")

    # Check if the sound file exists
    if not os.path.exists(sound_file):
        module.fail_json(msg=f"Sound file not found: {sound_file}")

    # Play the sound based on the platform
    system = platform.system()
    success = False
    
    # Check if we're in silent mode
    silent_mode = os.environ.get('ANSIBLE_BELL_SILENT') == 'true'
    
    if silent_mode:
        # Just pretend it worked in silent mode
        success = True
        module.log(msg=f"Silent mode: Would play sound {sound_file}")
    elif system == 'Darwin':  # macOS
        success = play_sound_macos(sound_file, volume)
    elif system == 'Linux':
        success = play_sound_linux(sound_file, volume)
    elif system == 'Windows':
        success = play_sound_windows(sound_file, volume)
    else:
        # For unsupported platforms, just log and continue
        module.log(msg=f"Unsupported platform: {system}, sound would play here")
        success = True

    if not success:
        # Don't fail the playbook, just warn
        module.warn(f"Failed to play sound on {system}")
        # Still mark as changed for idempotency
        success = True

    # Print the message
    if message:
        module.log(msg=message)

    module.exit_json(
        changed=True,
        message=message,
        sound_file=sound_file
    )


if __name__ == '__main__':
    main()