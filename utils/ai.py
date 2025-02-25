import os
import yaml
import requests
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEYS = {
    "gemini": os.getenv("GEMINI_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
    "groq": os.getenv("GROQ_API_KEY")
}

script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, '../config.json')

def load_config():
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_api_url(model_type, config):
    urls = {
        1: ("openai", config['openai_api_url'], config['openai_model']),
        2: ("groq", config['groq_api_url'], config['groq_model']),
        3: ("gemini", config['gemini_api_url'], None)
    }
    return urls.get(model_type, (None, None, None))

def validate_api_key(service):
    if not API_KEYS.get(service):
        print(f"Error: {service.upper()}_API_KEY not found in .env file")
        sys.exit(1)

def handle_gemini(logs, config, api_key):
    # Gemini doesn't support headers, so we pass the API key as a query parameter.
    data = {
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{config['prompt_message']}:\n\n{logs}"}]
        }]
    }
    api_url = f"{config['gemini_api_url']}?key={api_key}"
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    return None
def handle_openai(logs, config, api_key, model):
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": f"{config['prompt_message']}:\n\n{logs}"
        }]
    }
    response = requests.post(
        config['openai_api_url'],
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"[OpenAI] Request failed with status code {response.status_code}: {response.text}")
        return None

def handle_groq(logs, config, api_key, model):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{
            "role": "user",
            "content": f"{config['prompt_message']}:\n\n{logs}"
        }],
        "model": model
    }
    response = requests.post(
        config['groq_api_url'],
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"[Groq] Request failed with status code {response.status_code}: {response.text}")
        return None

def main():
    parser = argparse.ArgumentParser(description='WAID Log Summarizer')
    parser.add_argument('--ai', type=int, required=True,
                        choices=[1, 2, 3],
                        help='AI model selection: 1=ChatGPT, 2=Groq, 3=Gemini')
    args = parser.parse_args()

    config = load_config()
    service, api_url, model = get_api_url(args.ai, config)

    if not service:
        print("Invalid AI selection")
        sys.exit(1)

    validate_api_key(service)
    log_file_path = os.path.expanduser(config['log_file_path'])
    output_file_path = os.path.expanduser(config['output_file_path'])

    if not os.path.exists(log_file_path):
        print(f"Log file not found: {log_file_path}")
        sys.exit(1)

    try:
        with open(log_file_path, 'r') as file:
            logs = file.read()

        result = None
        if args.ai == 1:
            result = handle_openai(logs, config, API_KEYS[service], model)
        elif args.ai == 2:
            result = handle_groq(logs, config, API_KEYS[service], model)
        elif args.ai == 3:
            result = handle_gemini(logs, config, API_KEYS[service])

        if result:
            with open(output_file_path, 'w') as output_file:
                output_file.write(result)
            print("Summary generated successfully!")
        else:
            print("Failed to generate summary")

    except Exception as e:
        print(f"Error processing logs: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
