from jira import JIRA
from services.jira.config import JiraConfig

class JiraConnection:
    """Handles connection to the JIRA API"""

    def __init__(self, config=None):
        """Initialize JIRA connection using provided or default config"""
        self.config = config or JiraConfig()
        self.jira = None
        self.connect()

    def connect(self):
        """Establish connection to JIRA"""
        try:
            options = {"server": self.config.jira_domain}
            self.jira = JIRA(options, basic_auth=(self.config.jira_email, self.config.jira_api_token))

            # Get user info and handle both dictionary and object responses
            myself = self.jira.myself()
            if isinstance(myself, dict):
                display_name = myself.get('displayName', myself.get('name', 'Unknown User'))
            else:
                display_name = getattr(myself, 'displayName', getattr(myself, 'name', 'Unknown User'))

            print(f"Connected to JIRA as {display_name}")
            return True
        except Exception as e:
            print(f"Failed to connect to JIRA: {e}")
            return False

    def is_connected(self):
        """Check if connection to JIRA is established"""
        return self.jira is not None
