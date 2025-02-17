#!/bin/bash

# Path to the log file
LOG_FILE="$HOME/waid.log"

# Check if the log file exists and delete it
if [[ -f "$LOG_FILE" ]]; then
    rm "$LOG_FILE"
    echo "Logs have been cleared from $LOG_FILE"
else
    echo "No log file found at $LOG_FILE."
fi
