# play_sound

The `play_sound` module plays a sound when an Ansible task completes, providing audible notification for long-running playbooks.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| sound_file | str | no | (default sound) | Path to the sound file to play |
| message | str | no | "Ansible task completed" | Message to display along with the sound |
| volume | float | no | 1.0 | Volume level for the sound (0.0 to 1.0) |

## Examples

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

## Return Values

| Key | Type | Description |
|-----|------|-------------|
| message | str | The message that was displayed |
| sound_file | str | The sound file that was played |

## Notes

- On Linux, the module will try to use `aplay`, `paplay`, or `mplayer` (in that order)
- On macOS, the module uses `afplay`
- On Windows, the module uses PowerShell

## Requirements

- Python 3.6 or higher
- Appropriate sound player for your platform (see Notes)