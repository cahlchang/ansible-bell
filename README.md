# Ansible Bell

This repository contains the Ansible Bell collection (`cahlchang.bell`), which provides modules and plugins to play sounds when Ansible tasks complete.

## Features

- Play sounds when Ansible tasks complete
- Callback plugin to play sounds at playbook completion
- Cross-platform support (Linux, macOS, Windows)
- Customizable sounds and volume
- Built-in sample sounds that work out of the box

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

### Build from Source

```bash
# Clone the repository
git clone https://github.com/cahlchang/ansible-bell.git
cd ansible-bell
# Build the collection
ansible-galaxy collection build ansible_collections/cahlchang/bell
# Install the collection
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

The bell callback plugin works out of the box with built-in sample sounds. Simply enable it in your `ansible.cfg`:

```ini
[defaults]
callbacks_enabled = cahlchang.bell.bell
```

You can customize the sounds and volume by adding:

```ini
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