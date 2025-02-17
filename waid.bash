#!/bin/bash

# Path to the virtual environment
VENV_PATH="$HOME/Documents/waid/venv"

# Path to the log_summarizer.py script
SCRIPT_PATH="$HOME/Documents/waid/log_summarizer.py"

# Check if the virtual environment exists and activate it
if [[ -d "$VENV_PATH" ]]; then
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
    
    # Check if the log_summarizer.py script exists
    if [[ -f "$SCRIPT_PATH" ]]; then
        # Run the log_summarizer.py script
        python "$SCRIPT_PATH"
    else
        echo "log_summarizer.py not found at $SCRIPT_PATH."
    fi
    
    # Deactivate the virtual environment after the script runs
    deactivate
else
    echo "Virtual environment not found at $VENV_PATH."
fi
