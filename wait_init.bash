#!/bin/bash

# Ask the user to enter their Groq API key
echo "Please enter your Groq API key:"
read GROQ_API_KEY

# Path to the config.json file
CONFIG_FILE="$HOME/Documents/waid/config.json"

# Check if the config.json exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "config.json not found! Creating a new config.json file."
    # Create the JSON file with default values if it doesn't exist
    echo '{
  "log_file_path": "~/waid.log",
  "groq_api_url": "https://api.groq.com/openai/v1/chat/completions",
  "groq_api_key": "",
  "model": "llama-3.3-70b-versatile",
  "prompt_message": "Here are the logs of what all things I did today. Please check them and generate a JIRA ticket accordingly that I can directly enter into JIRA:"
}' > "$CONFIG_FILE"
fi

# Use jq to update the Groq API key in the JSON file
jq --arg GROQ_API_KEY "$GROQ_API_KEY" '.groq_api_key = $GROQ_API_KEY' "$CONFIG_FILE" > temp.json && mv temp.json "$CONFIG_FILE"

echo "Groq API key updated in $CONFIG_FILE."
