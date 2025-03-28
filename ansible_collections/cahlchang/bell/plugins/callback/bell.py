#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, cahlchang
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
    callback: bell
    type: notification
    short_description: Plays a sound when playbooks finish
    version_added: "1.0.0"
    description:
        - This callback plays a sound when playbooks finish.
        - The sound is played on the control node.
        - By default, it uses sample sounds included with the collection.
        - You can override the default sounds by specifying custom sound files in ansible.cfg.
    requirements:
        - A sound player (aplay, paplay, mplayer on Linux; afplay on macOS; PowerShell on Windows)
    options:
      success_sound:
        description: Path to sound file to play on successful playbook completion
        ini:
          - section: callback_bell
            key: success_sound
        env:
          - name: ANSIBLE_BELL_SUCCESS_SOUND
        type: path
      failure_sound:
        description: Path to sound file to play on failed playbook completion
        ini:
          - section: callback_bell
            key: failure_sound
        env:
          - name: ANSIBLE_BELL_FAILURE_SOUND
        type: path
      volume:
        description: Volume level for the sound (0.0 to 1.0)
        ini:
          - section: callback_bell
            key: volume
        env:
          - name: ANSIBLE_BELL_VOLUME
        type: float
        default: 1.0
'''

import os
import platform
import subprocess
import tempfile

from ansible.plugins.callback import CallbackBase
from ansible.module_utils.common.text.converters import to_text

# Try to import our module utils
try:
    from ansible_collections.cahlchang.bell.plugins.module_utils.sound_utils import (
        create_default_sound,
        get_default_sound_path,
    )
    HAS_SOUND_UTILS = True
except ImportError:
    HAS_SOUND_UTILS = False


class CallbackModule(CallbackBase):
    """
    Plays a sound when playbooks complete.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'cahlchang.bell.bell'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        
        self.success_sound = None
        self.failure_sound = None
        self.volume = 1.0
        
    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)
        
        self.success_sound = self.get_option('success_sound')
        self.failure_sound = self.get_option('failure_sound')
        self.volume = float(self.get_option('volume'))
        
        # Create default sounds if not specified
        if not self.success_sound or not os.path.exists(self.success_sound):
            if HAS_SOUND_UTILS:
                self.success_sound = create_default_sound('success')
            else:
                self.success_sound = self._create_default_sound()
                
        if not self.failure_sound or not os.path.exists(self.failure_sound):
            if HAS_SOUND_UTILS:
                self.failure_sound = create_default_sound('failure')
            else:
                self.failure_sound = self._create_default_sound()

    def _create_default_sound(self):
        """Create a default beep sound file."""
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

    def _play_sound(self, sound_file):
        """Play a sound file."""
        if not sound_file or not os.path.exists(sound_file):
            return
            
        system = platform.system()
        
        try:
            if system == 'Darwin':  # macOS
                subprocess.call(["afplay", "-v", str(self.volume), sound_file])
            elif system == 'Linux':
                # Try aplay first (ALSA)
                try:
                    subprocess.call(["aplay", "-q", sound_file])
                except Exception:
                    # Try paplay (PulseAudio)
                    try:
                        subprocess.call(["paplay", sound_file])
                    except Exception:
                        # Try mplayer
                        vol_percent = int(self.volume * 100)
                        subprocess.call(["mplayer", "-really-quiet", "-volume", str(vol_percent), sound_file])
            elif system == 'Windows':
                # PowerShell command to play sound
                ps_command = f'''
                Add-Type -AssemblyName presentationCore
                $mediaPlayer = New-Object system.windows.media.mediaplayer
                $mediaPlayer.Open("{sound_file}")
                $mediaPlayer.Volume = {self.volume}
                $mediaPlayer.Play()
                Start-Sleep -s 2  # Wait for sound to finish
                '''
                
                subprocess.call(["powershell", "-Command", ps_command])
        except Exception as e:
            self._display.warning(f"Failed to play sound: {to_text(e)}")

    def v2_playbook_on_stats(self, stats):
        """Play sound when playbook finishes."""
        failures = False
        unreachable = False
        
        for host in stats.processed.keys():
            summary = stats.summarize(host)
            if summary['failures'] > 0:
                failures = True
            if summary['unreachable'] > 0:
                unreachable = True
                
        if failures or unreachable:
            self._display.display("Playbook finished with failures or unreachable hosts")
            self._play_sound(self.failure_sound)
        else:
            self._display.display("Playbook finished successfully")
            self._play_sound(self.success_sound)