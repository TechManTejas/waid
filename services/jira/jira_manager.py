from services.jira.config import JiraConfig
from services.jira.connection import JiraConnection
from services.jira.ticket_fetcher import TicketFetcher
from services.jira.log_parser import LogParser
from services.jira.time_logger import TimeLogger
from services.jira.comment_manager import CommentManager
from services.jira.cli import JiraCLI

class JiraManager:
    """Main class that orchestrates all JIRA operations"""

    def __init__(self, jira_domain=None, jira_email=None, project_key=None, log_file=None):
        """Initialize with optional configuration parameters"""
        # Setup components
        self.config = JiraConfig(jira_domain, jira_email, project_key, log_file)
        self.connection = JiraConnection(self.config)
        self.ticket_fetcher = TicketFetcher(self.connection)
        self.log_parser = LogParser(self.config)
        self.time_logger = TimeLogger(self.connection)
        self.comment_manager = CommentManager(self.connection)
        self.cli = JiraCLI(self)

    def update_config(self, jira_domain=None, jira_email=None, project_key=None, log_file=None):
        """Update the configuration and reconnect if necessary"""
        config_updated = self.config.update_config(
            jira_domain=jira_domain,
            jira_email=jira_email,
            project_key=project_key,
            log_file=log_file
        )

        if config_updated and (jira_domain or jira_email):
            # If domain or email changes, reconnect
            print("Configuration updated, reconnecting...")
            self.connection = JiraConnection(self.config)

            # Recreate components that depend on connection
            self.ticket_fetcher = TicketFetcher(self.connection)
            self.time_logger = TimeLogger(self.connection)
            self.comment_manager = CommentManager(self.connection)

        return config_updated

    def run_cli(self):
        """Run the command-line interface"""
        return self.cli.run()

def main():
    """Entry point when module is run directly"""
    jira_manager = JiraManager()
    jira_manager.run_cli()

# Entry point for CLI usage
if __name__ == "__main__":
    main()
