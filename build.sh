#!/bin/bash

# Build and install the Ansible Bell collection

set -e

echo "Building Ansible Bell collection..."
cd "$(dirname "$0")"
ansible-galaxy collection build ansible_collections/cahlchang/bell --force

echo "Installing Ansible Bell collection..."
LATEST_BUILD=$(ls -t cahlchang-bell-*.tar.gz | head -n1)
ansible-galaxy collection install "$LATEST_BUILD" --force

echo "Installation complete!"
echo "You can now use the cahlchang.bell collection in your playbooks."