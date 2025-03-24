import os
import re
from datetime import datetime

class LogParser:
    """Parses log files for JIRA ticket creation/update"""

    def __init__(self, config):
        """Initialize with a JiraConfig instance"""
        self.config = config

    def parse_log(self):
        """Parse log file to extract ticket data"""
        if not os.path.exists(self.config.log_file):
            print("No logs found.")
            return None

        with open(self.config.log_file, "r") as f:
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

        return self.validate_and_transform_data(log_data)

    def validate_and_transform_data(self, log_data):
        """Validate and transform log data into JIRA compatible format"""
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
        log_data['start_time'] = log_data.get('Start time', '10:00:00')
        log_data['genai_use_case_desc'] = log_data['GenAI use case description']

        return log_data
