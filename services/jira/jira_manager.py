from enum import Enum
import base64
import requests
from datetime import datetime
from services.config.config_manager import ConfigManager


class JiraManagerConfig(Enum):
    BASE_URL = "jira_base_url"
    API_TOKEN = "jira_api_token"
    USER_EMAIL = "jira_user_email"
    DEFAULT_PROJECT_KEY = "jira_default_project_key"


class JiraManager:
    """Handles interactions with the Jira REST API."""

    @classmethod
    def set_configuration(cls, config_obj: dict):
        """
        Securely store the configuration parameters for Jira.
        """
        for key in JiraManagerConfig:
            if key.value in config_obj:
                ConfigManager.set(key.value, config_obj[key.value])

    @classmethod
    def get_configuration(cls) -> dict:
        """
        Retrieve stored Jira configuration.
        """
        return {
            key.value: ConfigManager.get(key.value)
            for key in JiraManagerConfig
        }

    @classmethod
    def get_required_configuration(cls) -> list:
        """
        Return a list of required configurations for Jira.
        """
        return [key.value for key in JiraManagerConfig]

    @classmethod
    def _get_auth_headers(cls):
        """Return authentication headers for Jira API."""
        token = ConfigManager.get(JiraManagerConfig.API_TOKEN.value)
        email = ConfigManager.get(JiraManagerConfig.USER_EMAIL.value)

        if not token or not email:
            raise ValueError("Jira API token or email not found in config.json")

        credentials = f"{email}:{token}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        return {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }

    @classmethod
    def _get_base_url(cls):
        url = ConfigManager.get(JiraManagerConfig.BASE_URL.value)
        if not url:
            raise ValueError("Jira base URL not found in config.json")
        return url.rstrip("/")

    @classmethod
    def _get_default_project_key(cls):
        key = ConfigManager.get(JiraManagerConfig.DEFAULT_PROJECT_KEY.value)
        if not key:
            raise ValueError("No default Jira project key set in config.json")
        return key

    @classmethod
    def get_my_issues(cls):
        """Fetch issues assigned to the current user."""
        url = f"{cls._get_base_url()}/rest/api/3/search"
        jql = "assignee = currentUser() ORDER BY updated DESC"

        response = requests.get(url, headers=cls._get_auth_headers(), params={"jql": jql})
        response.raise_for_status()
        return response.json().get("issues", [])

    @classmethod
    def create_issue(cls, summary: str, description: str, project_key: str = None, issue_type: str = "Task"):
        """Create a new Jira issue. If no project_key is provided, use the default."""
        if not project_key:
            project_key = cls._get_default_project_key()

        url = f"{cls._get_base_url()}/rest/api/3/issue"

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type}
            }
        }

        response = requests.post(url, headers=cls._get_auth_headers(), json=payload)
        response.raise_for_status()
        return response.json()

    @classmethod
    def add_comment(cls, issue_key: str, comment: str):
        """Add a comment to a Jira issue."""
        url = f"{cls._get_base_url()}/rest/api/3/issue/{issue_key}/comment"
        payload = {"body": comment}

        response = requests.post(url, headers=cls._get_auth_headers(), json=payload)
        response.raise_for_status()
        return response.json()

    @classmethod
    def log_work(cls, issue_key: str, time_spent: str, comment: str = "", started: datetime = None):
        """Log time spent on a Jira issue."""
        url = f"{cls._get_base_url()}/rest/api/3/issue/{issue_key}/worklog"

        worklog = {
            "timeSpent": time_spent,
        }

        if comment:
            worklog["comment"] = comment
        if started:
            worklog["started"] = started.strftime("%Y-%m-%dT%H:%M:%S.000+0000")

        response = requests.post(url, headers=cls._get_auth_headers(), json=worklog)
        response.raise_for_status()
        return response.json()
