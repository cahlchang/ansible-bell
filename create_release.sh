#!/bin/bash

# Script to create a new release tag

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.1"
    exit 1
fi

VERSION=$1

# Validate version format
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format X.Y.Z (e.g., 1.0.1)"
    exit 1
fi

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "Error: Working directory is not clean. Commit or stash changes first."
    exit 1
fi

# Create and push tag
echo "Creating tag v$VERSION..."
git tag -a "v$VERSION" -m "Release v$VERSION"
echo "Pushing tag to remote repository..."
git push origin "v$VERSION"

echo "Tag v$VERSION created and pushed."
echo "GitHub Actions workflow will automatically create a release with the built collection."
echo "Check the status at: https://github.com/cahlchang/ansible-bell/actions"