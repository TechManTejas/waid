from jira import JIRA
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Jira Configuration
JIRA_DOMAIN = "https://qed42-operations.atlassian.net"
JIRA_EMAIL = "tejas.vaij@qed42.com"
JIRA_API_TOKEN =  os.getenv("JIRA_API_KEY")
PROJECT_KEY = "QWDI"

# Connect to Jira
options = {"server": JIRA_DOMAIN}
jira = JIRA(options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

# Fetch Kanban tickets assigned to you that are in To Do or In Progress
def fetch_my_kanban_tickets():
    jql_query = f'project = "{PROJECT_KEY}" AND assignee = currentUser() AND status IN ("PR Review") ORDER BY rank ASC'
    issues = jira.search_issues(jql_query, maxResults=100)

    tickets = []
    for issue in issues:
        tickets.append({
            "key": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
        })

    return tickets

if __name__ == "__main__":
    tickets = fetch_my_kanban_tickets()
    for ticket in tickets:
        print(f"{ticket['key']}: {ticket['summary']} - {ticket['status']} (Assigned to: {ticket['assignee']})")