#!/bin/bash

SOURCE_FILE="$1"
DESTINATION_DIR="/opt/main"
LOG_FILE="/var/log/update_success.log"

echo "Starting update process..." | sudo tee -a "$LOG_FILE"

if [ -f "$SOURCE_FILE" ]; then
    echo "Source file found at $SOURCE_FILE" | sudo tee -a "$LOG_FILE"
    sudo cp "$SOURCE_FILE" "$DESTINATION_DIR/main" && echo "Update completed successfully at $(date)" | sudo tee -a "$LOG_FILE"
else
    echo "Source file not found: $SOURCE_FILE" | sudo tee -a "$LOG_FILE"
    exit 1
fi
