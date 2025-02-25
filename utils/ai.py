import os
import yaml
import requests
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, '../config.json')

def load_config():
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Load configuration
config = load_config()

# Expand the log file path to handle ~ (home directory)
log_file_path = os.path.expanduser(config['log_file_path'])

# Define the output file in the home directory
output_file_path = os.path.expanduser("~/waid_summary.log")

# Redirect stdout to the log file
with open(output_file_path, 'w') as output_file:
    sys.stdout = output_file  # Redirect stdout to file

    # Check if the log file exists
    if os.path.exists(log_file_path):
        try:
            # Open and read the log file
            with open(log_file_path, 'r') as file:
                logs = file.read()
                # print("Logs from waid.log:")
                # print(logs)

                # Prepare the request payload for Gemini Flash 2
                data = {
                    "contents": [{
                        "role": "user",
                        "parts": [{"text": f"{config['prompt_message']}:\n\n{logs}"}]
                    }]
                }

                #  headers = {
                #     "Authorization": f"Bearer {GEMINI_API_KEY}",
                #     "Content-Type": "application/json"
                # }
                api_url = f"{config['gemini_api_url']}?key={GEMINI_API_KEY}"
                # Send logs and prompt to Gemini API
                response = requests.post(api_url, json=data)
                # Check if the request was successful
                if response.status_code == 200:
                    gemini_response = response.json()

                    # Extract and format the response for the JIRA ticket
                    ticket_content = gemini_response['candidates'][0]['content']['parts'][0]['text']

                    # print("\nGenerated JIRA Ticket Based on Logs:")
                    print(ticket_content)
                else:
                    print(f"Failed to send logs to Gemini. Status code: {response.status_code}")
                    print(response.text)
        except Exception as e:
            print(f"Error reading the log file: {e}")
    else:
        print(f"No logs found. The file {log_file_path} does not exist.")

# Restore stdout back to default
sys.stdout = sys.__stdout__
