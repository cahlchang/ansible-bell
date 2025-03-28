# Ansible Bell

This repository contains the Ansible Bell collection (`cahlchang.bell`), which provides modules and plugins to play sounds when Ansible tasks complete.

## Features

- Play sounds when Ansible tasks complete
- Callback plugin to play sounds at playbook completion
- Cross-platform support (Linux, macOS, Windows)
- Customizable sounds and volume

## Installation

```bash
ansible-galaxy collection install cahlchang.bell
```

Or, clone this repository and build the collection:

```bash
cd ansible-bell
ansible-galaxy collection build ansible_collections/cahlchang/bell
ansible-galaxy collection install cahlchang-bell-*.tar.gz
```

## Usage

### Using the play_sound module

```yaml
- name: Play a sound after deployment
  cahlchang.bell.play_sound:
    message: "Deployment completed successfully"
```

### Using the bell callback plugin

Add to your `ansible.cfg`:

```ini
[defaults]
callback_whitelist = cahlchang.bell.bell

[callback_bell]
success_sound = /path/to/success.wav
failure_sound = /path/to/failure.wav
volume = 0.8
```

## Documentation

See the [collection documentation](ansible_collections/cahlchang/bell/README.md) for more details.

## License

GNU General Public License v3.0 or later

## Author

- cahlchang (@cahlchang)