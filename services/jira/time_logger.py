import requests

class TimeLogger:
    """Logs time to JIRA/Tempo"""

    def __init__(self, connection):
        """Initialize with a JiraConnection instance"""
        self.connection = connection

    def log_time(self, issue_key, log_data):
        """Log time to JIRA using Tempo API"""
        if not self.connection.is_connected():
            print("Not connected to JIRA")
            return False

        try:
            issue = self.connection.jira.issue(issue_key)
            headers = {
                "Authorization": f"Bearer {self.connection.config.tempo_api_token}",
                "Content-Type": "application/json",
            }

            worklog_data = {
                "issueId": issue.id,
                "timeSpentSeconds": log_data['duration_seconds'],
                "startDate": log_data['start_date'],
                "startTime": log_data['start_time'],
                "description": log_data['summary'],
                "authorAccountId": self.connection.jira.myself().get("accountId"),
                "attributes": [
                    {"key": "_GenAIEfficiency_", "value": log_data['genai_efficiency']},
                    {"key": "_GenAIusecasedescription_", "value": log_data['genai_use_case_desc']},
                ],
            }

            response = requests.post(
                self.connection.config.tempo_api_url,
                json=worklog_data,
                headers=headers
            )

            if response.status_code in [200, 201]:
                print(f"Time logged successfully to {issue_key}.")
                return True
            else:
                print(f"Failed to log time: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error logging time: {e}")
            return False
