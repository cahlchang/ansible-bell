# Sample Sounds

This directory contains sample sound files that are used by default in the Ansible Bell collection.

## Files

- `success_sound.wav` - Played when a playbook completes successfully
- `failure_sound.wav` - Played when a playbook fails

## Usage

These sounds are used automatically by the bell callback plugin when no custom sounds are specified in your `ansible.cfg` file.

## Customization

You can override these default sounds by specifying custom sound files in your `ansible.cfg`:

```ini
[callback_bell]
success_sound = /path/to/your/success.wav
failure_sound = /path/to/your/failure.wav
```

## License

These sound files are provided under the same license as the Ansible Bell collection (GNU General Public License v3.0 or later).