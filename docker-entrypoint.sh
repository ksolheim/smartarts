#!/bin/bash
set -e

# Get current UID and GID from environment variables or use defaults
USER_ID=${LOCAL_UID:-1000}
GROUP_ID=${LOCAL_GID:-1000}

echo "Starting with UID: $USER_ID, GID: $GROUP_ID"

# Update the user and group IDs
groupmod -g $GROUP_ID smartarts
usermod -u $USER_ID -g $GROUP_ID smartarts

# Update ownership of relevant directories
chown -R smartarts:smartarts /app/database

# Execute the command as the smartarts user
exec gosu smartarts "$@" 