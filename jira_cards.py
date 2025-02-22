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

def summarize_logs():
    if not os.path.exists(LOG_FILE):
        print("No logs found.")
        return None

    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    log_entries = []
    tasks = set()

    for log in logs:
        match = re.search(r"\{.*\}", log)
        if match:
            try:
                entry = json.loads(match.group())
                log_entries.append(entry)
                if "window_title" in entry:
                    tasks.add(entry["window_title"])
            except json.JSONDecodeError:
                continue

    if len(log_entries) < 2:
        print("Not enough valid log entries found.")
        return None

    start_time = log_entries[0]["timestamp"]
    end_time = log_entries[-1]["timestamp"]

    try:
        duration = (
            datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            - datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        ).total_seconds() / 60
    except ValueError as e:
        print("Timestamp parsing error:", e)
        return None

    if duration < 1:
        print("Duration too short to log work.")
        return None

    description = "\n".join(f"* Worked on `{task}`" for task in tasks)

    return {
        "summary": "Work on JIRA Cards and Log Summarizer",
        "description": description,
        "duration": duration,
        "start_time": start_time,
        "end_time": end_time,
        "date": start_time.split(" ")[0],
        "genai_efficiency": round(duration / 60, 2),
    }

def log_time_to_jira(
    issue_key, summary, duration, start_date, genai_efficiency=0, genai_use_case_desc=""):
    issue = jira.issue(issue_key)
    issue_id = issue.id  # Get issue ID

    worklog_data = {
        "issueId": issue_id,
        "timeSpentSeconds": int(duration * 60),
        "startDate": start_date,
        "description": summary,
        "authorAccountId": jira.myself().get("accountId"),
        "attributes": [
            {"key": "_GenAIEfficiency_", "value": genai_efficiency},
            {"key": "_GenAIusecasedescription_", "value": genai_use_case_desc},
        ],
    }

    headers = {
        "Authorization": f"Bearer {TEMPO_API_TOKEN}",
        "Content-Type": "application/json",
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

    log_summary = summarize_logs()
    if log_summary:
        log_time_to_jira(
            selected_ticket["key"],
            log_summary["summary"],
            log_summary["duration"],
            log_summary["date"],
            log_summary["genai_efficiency"],
            genai_use_case_desc="Worked on issue-related tasks"
        )
