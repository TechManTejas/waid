from jira import JIRA
from dotenv import load_dotenv
import os
import json
import requests
import re
from datetime import datetime

# Load environment variables
load_dotenv()

# API Tokens
JIRA_API_TOKEN = os.getenv("JIRA_API_KEY")
TEMPO_API_TOKEN = os.getenv("TEMPO_API_KEY")

# Jira Configuration
JIRA_DOMAIN = "https://qed42-operations.atlassian.net"
JIRA_EMAIL = "vaibhav.sapate@qed42.com"
PROJECT_KEY = "AT"
TEMPO_API_URL = "https://api.tempo.io/4/worklogs"
LOG_FILE = os.path.expanduser("~/waid_summary.log")

# Connect to Jira
options = {"server": JIRA_DOMAIN}
jira = JIRA(options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

def fetch_my_kanban_tickets():
    jql_query = f'project = "{PROJECT_KEY}" AND assignee = currentUser() AND status IN ("In Progress") ORDER BY created DESC'
    try:
        issues = jira.search_issues(jql_query, maxResults=10)
    except Exception as e:
        print("Jira API Error:", e)
        return []
    return [
        {"id": idx, "key": issue.key, "summary": issue.fields.summary}
        for idx, issue in enumerate(issues, 1)
    ]

def parse_log():
    if not os.path.exists(LOG_FILE):
        print("No logs found.")
        return None

    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    log_data = {}
    current_field = None
    lines = log_content.split('\n')

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            current_field = None
            continue

        field_match = re.match(r'^([A-Za-z\s]+):\s*(.*)', line)
        if field_match:
            current_field = field_match.group(1).strip()
            value = field_match.group(2).strip()

            if current_field == 'Description':
                log_data[current_field] = [value] if value else []
            else:
                log_data[current_field] = value
        else:
            if current_field == 'Description' and current_field in log_data:
                log_data[current_field].append(stripped_line)

    if 'Description' in log_data:
        log_data['Description'] = '\n'.join(log_data['Description'])

    required_fields = ['Title', 'Description', 'Date', 'Duration', 'Start time',
                      'GenAI Efficiency', 'GenAI use case description']
    for field in required_fields:
        if field not in log_data:
            print(f"Missing required field in log: {field}")
            return None

    try:
        date_str = log_data['Date']
        parsed_date = datetime.strptime(date_str, "%d/%b/%y")
        log_data['start_date'] = parsed_date.strftime("%Y-%m-%d")
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

    try:
        duration_hours = float(log_data['Duration'])
        log_data['duration_seconds'] = int(duration_hours * 3600)
    except ValueError as e:
        print(f"Error parsing duration: {e}")
        return None

    try:
        log_data['genai_efficiency'] = float(log_data['GenAI Efficiency'])
    except ValueError as e:
        print(f"Error parsing GenAI Efficiency: {e}")
        return None

    log_data['summary'] = log_data.get('Summary', 'Work Log Summary')
    log_data['start_time'] = log_data.get('Start time', '00:00:00')
    log_data['genai_use_case_desc'] = log_data['GenAI use case description']

    return log_data

def log_time_to_jira(issue_key, log_data):
    issue = jira.issue(issue_key)
    headers = {
        "Authorization": f"Bearer {TEMPO_API_TOKEN}",
        "Content-Type": "application/json",
    }

    worklog_data = {
        "issueId": issue.id,
        "timeSpentSeconds": log_data['duration_seconds'],
        "startDate": log_data['start_date'],
        "startTime": log_data['start_time'],
        "description": log_data['summary'],
        "authorAccountId": jira.myself().get("accountId"),
        "attributes": [
            {"key": "_GenAIEfficiency_", "value": log_data['genai_efficiency']},
            {"key": "_GenAIusecasedescription_", "value": log_data['genai_use_case_desc']},
        ],
    }

    response = requests.post(TEMPO_API_URL, json=worklog_data, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Time logged successfully to {issue_key}.")
    else:
        print(f"Failed to log time: {response.status_code} - {response.text}")

if __name__ == "__main__":
    tickets = fetch_my_kanban_tickets()
    if not tickets:
        print("No active tickets found.")
        exit()

    print("Here are your active tickets. Enter the number to log time:")
    for ticket in tickets:
        print(f"{ticket['id']}. {ticket['key']} - {ticket['summary']}")

    try:
        choice = int(input("Enter ticket number: ")) - 1
        selected_ticket = tickets[choice]
    except (ValueError, IndexError):
        print("Invalid selection.")
        exit()

    log_data = parse_log()
    if not log_data:
        print("Failed to process log file.")
        exit()

    # Add comment to Jira ticket
    try:
        issue = jira.issue(selected_ticket["key"])
        comment_body = f"h3. {log_data['Title']}\n\n{log_data['Description']}"
        jira.add_comment(issue, comment_body)
        print(f"Added comment to {selected_ticket['key']}")
    except Exception as e:
        print(f"Failed to add comment: {e}")

    # Log time to Tempo
    log_time_to_jira(selected_ticket["key"], log_data)
