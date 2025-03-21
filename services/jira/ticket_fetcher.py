class TicketFetcher:
    """Fetches tickets from JIRA with status-based filtering"""

    def __init__(self, connection):
        """Initialize with a JiraConnection instance"""
        self.connection = connection
        self.categories = []  # Store fetched categories
        self.tickets = []     # Store fetched tickets

    def fetch_issue_categories(self):
        """Fetch available issue statuses that have tickets assigned to current user"""
        if not self.connection.is_connected():
            print("Not connected to JIRA")
            return []

        try:
            # Get all statuses for the user's tickets (not just In Progress)
            jql_query = f'project = "{self.connection.config.project_key}" AND assignee = currentUser()'
            issues = self.connection.jira.search_issues(jql_query, maxResults=50)

            # Extract unique statuses
            categories = {}
            for issue in issues:
                status = issue.fields.status
                if status.id not in categories:
                    categories[status.id] = {
                        "id": status.id,
                        "name": status.name,
                        "description": getattr(status, "description", ""),
                        "icon_url": getattr(status, "iconUrl", "")
                    }

            # Convert to list and sort by workflow order if possible
            self.categories = sorted(list(categories.values()), key=lambda x: x["name"])
            return self.categories

        except Exception as e:
            print(f"Error fetching status categories: {e}")
            return []

    def fetch_tickets_by_category(self, status_id):
        """Fetch tickets assigned to current user in a specific status"""
        if not self.connection.is_connected():
            print("Not connected to JIRA")
            return []

        try:
            # Get status name for the query
            status_name = next((cat["name"] for cat in self.categories if cat["id"] == status_id), None)
            if not status_name:
                print(f"Status ID {status_id} not found in categories")
                return []

            # Build query to find tickets in selected status
            jql_query = (f'project = "{self.connection.config.project_key}" AND '
                         f'status = "{status_name}" AND '
                         f'assignee = currentUser() '
                         f'ORDER BY created DESC')

            issues = self.connection.jira.search_issues(jql_query, maxResults=20)

            # Transform issues to a more usable format
            self.tickets = [
                {"id": idx, "key": issue.key, "summary": issue.fields.summary, "jira_obj": issue}
                for idx, issue in enumerate(issues, 1)
            ]
            return self.tickets
        except Exception as e:
            print(f"Error fetching tickets for status {status_id}: {e}")
            return []

    def get_ticket_details(self, ticket_key):
        """Get detailed information about a specific ticket"""
        if not self.connection.is_connected():
            print("Not connected to JIRA")
            return None

        try:
            # Find the ticket in our cached results first
            for ticket in self.tickets:
                if ticket["key"] == ticket_key:
                    issue = ticket["jira_obj"]
                    break
            else:
                # If not found in cache, fetch from API
                issue = self.connection.jira.issue(ticket_key)

            # Extract detailed information
            details = {
                "key": issue.key,
                "summary": issue.fields.summary,
                "description": issue.fields.description or "No description provided",
                "issue_type": issue.fields.issuetype.name,
                "status": issue.fields.status.name,
                "assignee": getattr(issue.fields.assignee, "displayName", "Unassigned"),
                "reporter": getattr(issue.fields.reporter, "displayName", "Unknown"),
                "created": issue.fields.created,
                "priority": getattr(issue.fields.priority, "name", "Not set"),
            }

            # Add labels if available
            if hasattr(issue.fields, "labels") and issue.fields.labels:
                details["labels"] = issue.fields.labels

            # Add components if available
            if hasattr(issue.fields, "components") and issue.fields.components:
                details["components"] = [c.name for c in issue.fields.components]

            return details
        except Exception as e:
            print(f"Error fetching details for ticket {ticket_key}: {e}")
            return None

    def fetch_my_kanban_tickets(self):
        """Legacy method that fetches all tickets across statuses"""
        if not self.connection.is_connected():
            print("Not connected to JIRA")
            return []

        jql_query = f'project = "{self.connection.config.project_key}" AND assignee = currentUser() ORDER BY created DESC'
        try:
            issues = self.connection.jira.search_issues(jql_query, maxResults=10)
            self.tickets = [
                {"id": idx, "key": issue.key, "summary": issue.fields.summary, "jira_obj": issue}
                for idx, issue in enumerate(issues, 1)
            ]
            return self.tickets
        except Exception as e:
            print("Jira API Error:", e)
            return []
