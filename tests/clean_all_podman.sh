#!/usr/bin/env bash

# Function to display usage
usage() {
  echo "Usage: $0 [-f]"
  echo "  -f    Force remove all containers and images, regardless of who created them"
  exit 1
}

# Check for the -f flag
force_remove=false

while getopts "f" opt; do
  case ${opt} in
    f)
      force_remove=true
      ;;
    *)
      usage
      ;;
  esac
done

# Stop all running containers
echo "Stopping all running containers..."
podman stop $(podman ps -q) 2>/dev/null

# Remove all containers
echo "Removing all containers..."
if [ "$force_remove" = true ]; then
  # Force remove all containers
  podman rm -f $(podman ps -a -q) 2>/dev/null
else
  # Remove containers normally
  podman rm $(podman ps -a -q) 2>/dev/null
fi

# Remove all images
echo "Removing all images..."
if [ "$force_remove" = true ]; then
  # Force remove all images
  podman rmi -f $(podman images -q) 2>/dev/null
else
  # Remove images normally
  podman rmi $(podman images -q) 2>/dev/null
fi

echo "Cleanup complete!"
