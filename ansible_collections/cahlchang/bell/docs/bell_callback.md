# Bell Callback Plugin

The `bell` callback plugin plays a sound when playbooks finish, providing audible notification for playbook completion.

## Configuration

You can configure the plugin in your `ansible.cfg` file:

```ini
[defaults]
callback_whitelist = cahlchang.bell.bell

[callback_bell]
success_sound = /path/to/success.wav
failure_sound = /path/to/failure.wav
volume = 0.8
```

Or using environment variables:

```bash
export ANSIBLE_CALLBACK_WHITELIST=cahlchang.bell.bell
export ANSIBLE_BELL_SUCCESS_SOUND=/path/to/success.wav
export ANSIBLE_BELL_FAILURE_SOUND=/path/to/failure.wav
export ANSIBLE_BELL_VOLUME=0.8
```

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| success_sound | path | no | (default sound) | Path to sound file to play on successful playbook completion |
| failure_sound | path | no | (default sound) | Path to sound file to play on failed playbook completion |
| volume | float | no | 1.0 | Volume level for the sound (0.0 to 1.0) |

## Notes

- If no sound files are specified, default beep sounds will be generated
- The plugin will try to use the appropriate sound player for your platform:
  - Linux: `aplay`, `paplay`, or `mplayer`
  - macOS: `afplay`
  - Windows: PowerShell

## Requirements

- Python 3.6 or higher
- Appropriate sound player for your platform (see Notes)