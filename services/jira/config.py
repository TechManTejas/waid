import os
import json
from pathlib import Path
from dotenv import load_dotenv

class JiraConfig:
    """Manages JIRA configuration and API tokens with persistent user settings"""

    # Default config path in user's home directory
    CONFIG_DIR = Path.home() / ".config" / "waid"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self, jira_domain=None, jira_email=None, project_key=None, log_file=None):
        # Load environment variables
        load_dotenv()

        # Load user config or create default
        self.user_config = self.load_user_config()

        # API Tokens
        self.jira_api_token = os.getenv("JIRA_API_KEY")
        self.tempo_api_token = os.getenv("TEMPO_API_KEY")

        # Jira Configuration - priorities:
        # 1. Constructor args, 2. User config, 3. Environment/defaults
        self.jira_domain = jira_domain or self.user_config.get("jira_domain") or "https://qed42-operations.atlassian.net"
        self.jira_email = jira_email or self.user_config.get("jira_email") or os.getenv("JIRA_EMAIL") or "vaibhav.sapate@qed42.com"
        self.project_key = project_key or self.user_config.get("project_key") or os.getenv("JIRA_PROJECT") or "AT"

        self.tempo_api_url = "https://api.tempo.io/4/worklogs"
        self.log_file = log_file or self.user_config.get("log_file") or os.path.expanduser("~/waid_summary.log")

        # Save any new values provided in constructor
        if jira_email or project_key or jira_domain or log_file:
            self.save_user_config()

    def load_user_config(self):
        """Load user configuration from JSON file"""
        try:
            # Create config directory if it doesn't exist
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            # If config file exists, load it
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            else:
                # Create default config file
                default_config = {}
                with open(self.CONFIG_FILE, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            print(f"Error loading user config: {e}")
            return {}

    def save_user_config(self):
        """Save current configuration to JSON file"""
        try:
            config_data = {
                "jira_domain": self.jira_domain,
                "jira_email": self.jira_email,
                "project_key": self.project_key,
                "log_file": self.log_file
            }

            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config_data, f, indent=4)
            print(f"Configuration saved to {self.CONFIG_FILE}")
            return True
        except Exception as e:
            print(f"Error saving user config: {e}")
            return False

    def update_config(self, **kwargs):
        """Update configuration with new values"""
        updated = False

        if "jira_domain" in kwargs and kwargs["jira_domain"]:
            self.jira_domain = kwargs["jira_domain"]
            updated = True

        if "jira_email" in kwargs and kwargs["jira_email"]:
            self.jira_email = kwargs["jira_email"]
            updated = True

        if "project_key" in kwargs and kwargs["project_key"]:
            self.project_key = kwargs["project_key"]
            updated = True

        if "log_file" in kwargs and kwargs["log_file"]:
            self.log_file = kwargs["log_file"]
            updated = True

        if updated:
            return self.save_user_config()
        return False
