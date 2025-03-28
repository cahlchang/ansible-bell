#!/bin/bash

# Build the Ansible Bell collection

set -e

echo "Building Ansible Bell collection..."
cd "$(dirname "$0")"
ansible-galaxy collection build ansible_collections/cahlchang/bell --force

LATEST_BUILD=$(ls -t cahlchang-bell-*.tar.gz | head -n1)
echo "Build complete: $LATEST_BUILD"
echo "To install the collection, run: ansible-galaxy collection install $LATEST_BUILD"