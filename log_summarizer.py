import os
import yaml
import requests

script_dir = os.path.dirname(os.path.realpath(__file__)) 
config_path = os.path.join(script_dir, 'config.json') 

def load_config():
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Load configuration
config = load_config()

# Expand the log file path to handle ~ (home directory)
log_file_path = os.path.expanduser(config['log_file_path'])

# Fetch Groq API URL and API key from the YAML config
groq_api_url = config['groq_api_url']
groq_api_key = config['groq_api_key']
model = config['model']
prompt_message = config['prompt_message']

# Check if the log file exists
if os.path.exists(log_file_path):
    try:
        # Open and read the log file
        with open(log_file_path, 'r') as file:
            logs = file.read()
            print("Logs from waid.log:")
            print(logs)

            # Prepare the request payload
            data = {
                "model": model,  # specify model from config
                "messages": [
                    {
                        "role": "user",
                        "content": f"{prompt_message}:\n\n{logs}"
                    }
                ]
            }

            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }

            # Send logs and prompt to Groq
            response = requests.post(groq_api_url, json=data, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                groq_response = response.json()
                
                # Extract and format the response for the JIRA ticket
                ticket_content = groq_response['choices'][0]['message']['content']

                print("\nGenerated JIRA Ticket Based on Logs:")
                print(ticket_content)
            else:
                print(f"Failed to send logs to Groq. Status code: {response.status_code}")
                print(response.text)
    except Exception as e:
        print(f"Error reading the log file: {e}")
else:
    print(f"No logs found. The file {log_file_path} does not exist.")
