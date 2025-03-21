class CommentManager:
    """Manages comments on JIRA tickets"""

    def __init__(self, connection):
        """Initialize with a JiraConnection instance"""
        self.connection = connection

    def add_comment(self, issue_key, title, description):
        """Add a formatted comment to a JIRA ticket"""
        if not self.connection.is_connected():
            print("Not connected to JIRA")
            return False

        try:
            issue = self.connection.jira.issue(issue_key)
            comment_body = f"h3. {title}\n\n{description}"
            self.connection.jira.add_comment(issue, comment_body)
            print(f"Added comment to {issue_key}")
            return True
        except Exception as e:
            print(f"Failed to add comment: {e}")
            return False
