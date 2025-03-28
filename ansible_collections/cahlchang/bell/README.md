# Ansible Bell Collection

This collection provides modules to play sounds when Ansible tasks complete, providing audible notifications for long-running playbooks. It includes built-in sample sounds that work out of the box, with the ability to customize sounds through configuration.

## Installation

### From Ansible Galaxy

```bash
ansible-galaxy collection install cahlchang.bell
```

### From GitHub Releases

```bash
# Download the latest release
curl -LO "https://github.com/cahlchang/ansible-bell/releases/latest/download/cahlchang-bell-latest.tar.gz"
# Install the collection
ansible-galaxy collection install cahlchang-bell-latest.tar.gz
```

## Modules

### play_sound

Play a sound when an Ansible task completes.

## Callback Plugins

### bell

The bell callback plugin plays sounds when playbooks finish. It uses built-in sample sounds by default, but you can customize the sounds through your `ansible.cfg` file.

#### Configuration

Add to your `ansible.cfg`:

```ini
[defaults]
callbacks_enabled = cahlchang.bell.bell

[callback_bell]
success_sound = /path/to/success.wav  # Optional, uses built-in sample sound if not specified
failure_sound = /path/to/failure.wav  # Optional, uses built-in sample sound if not specified
volume = 0.8  # Optional, defaults to 1.0
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| sound_file | str | no | (default sound) | Path to the sound file to play |
| message | str | no | "Ansible task completed" | Message to display along with the sound |
| volume | float | no | 1.0 | Volume level for the sound (0.0 to 1.0) |

#### Environment Variables

| Variable | Description |
|----------|-------------|
| ANSIBLE_BELL_SILENT | Set to "true" to disable sound playback (useful in CI/CD environments) |

#### Examples

```yaml
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
```

## Platform Support

- Linux: Uses `aplay`, `paplay`, or `mplayer` (whichever is available)
- macOS: Uses `afplay`
- Windows: Uses PowerShell

## License

GNU General Public License v3.0 or later

## Author

- cahlchang (@cahlchang)