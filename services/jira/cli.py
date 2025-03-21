class JiraCLI:
    """Command-line interface for JIRA interactions"""

    def __init__(self, jira_manager):
        """Initialize with a JiraManager instance"""
        self.jira_manager = jira_manager

    def configure(self):
        """Interactive configuration update"""
        print("\n=== JIRA Configuration ===")
        print(f"Current email: {self.jira_manager.config.jira_email}")
        print(f"Current project key: {self.jira_manager.config.project_key}")
        print(f"Current domain: {self.jira_manager.config.jira_domain}")
        print(f"Current log file: {self.jira_manager.config.log_file}")
        print("\nEnter new values (or leave blank to keep current):")

        email = input("JIRA Email: ").strip() or None
        project_key = input("Project Key: ").strip() or None
        domain = input("JIRA Domain: ").strip() or None
        log_file = input("Log File Path: ").strip() or None

        if self.jira_manager.update_config(
            jira_email=email,
            project_key=project_key,
            jira_domain=domain,
            log_file=log_file,
        ):
            print("Configuration updated successfully!")
        else:
            print("No changes were made to configuration.")

    def run(self):
        """Run the CLI workflow with configuration option"""
        print("\nWAID - JIRA Time Logging Tool")
        print("1. Log time to a ticket")
        print("2. Configure settings")
        print("3. Exit")

        choice = input("\nSelect an option (1-3): ")

        if choice == "1":
            return self._log_time_workflow()
        elif choice == "2":
            self.configure()
            return True
        elif choice == "3":
            print("Exiting...")
            return False
        else:
            print("Invalid option, please try again.")
            return self.run()

    def _log_time_workflow(self):
        """Enhanced workflow for logging time with category selection"""
        # Step 1: Fetch categories
        categories = self.jira_manager.ticket_fetcher.fetch_issue_categories()
        if not categories:
            print("No categories with active tickets found.")
            return False

        # Display categories
        print("\n=== Available Ticket Statuses ===")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category['name']}")

        # Get user's category selection
        try:
            cat_choice = int(input("\nSelect a status (or 0 to cancel): "))
            if cat_choice == 0:
                return True

            selected_category = categories[cat_choice - 1]
            print(f"\nSelected: {selected_category['name']}")
        except (ValueError, IndexError):
            print("Invalid selection.")
            return False

        # Step 2: Fetch tickets in selected category
        tickets = self.jira_manager.ticket_fetcher.fetch_tickets_by_category(
            selected_category["id"]
        )
        if not tickets:
            print(f"No active tickets found in category {selected_category['name']}.")
            return False

        # Display tickets
        print("\n=== Your Tickets in This Category ===")
        for ticket in tickets:
            print(f"{ticket['id']}. {ticket['key']} - {ticket['summary']}")

        # Get user's ticket selection
        try:
            ticket_choice = int(input("\nSelect a ticket (or 0 to cancel): "))
            if ticket_choice == 0:
                return True

            selected_ticket = tickets[ticket_choice - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return False

        # Step 3: Display ticket details
        details = self.jira_manager.ticket_fetcher.get_ticket_details(
            selected_ticket["key"]
        )
        if details:
            print("\n=== Ticket Details ===")
            print(f"Key: {details['key']}")
            print(f"Summary: {details['summary']}")
            print(f"Type: {details['issue_type']}")
            print(f"Status: {details['status']}")
            print(f"Assignee: {details['assignee']}")
            print(f"Priority: {details['priority']}")

            if "labels" in details:
                print(f"Labels: {', '.join(details['labels'])}")

            if "components" in details:
                print(f"Components: {', '.join(details['components'])}")

            print("\nDescription (excerpt):")
            description = details["description"]
            if description and len(description) > 200:
                print(f"{description[:200]}...")
            else:
                print(description or "No description")

            # Enhanced input handling with more flexible affirmative responses
            proceed = (
                input("\nProceed with logging time to this ticket? (Y/n): ")
                .lower()
                .strip()
            )
            affirmative_responses = ["y", "yes", "", "true", "t", "1"]

            if proceed not in affirmative_responses:
                print("Time logging canceled.")
                return True

        # Step 4: Parse log data
        log_data = self.jira_manager.log_parser.parse_log()
        if not log_data:
            print("Failed to process log file.")
            return False

        # Step 5: Add comment to Jira ticket
        self.jira_manager.comment_manager.add_comment(
            selected_ticket["key"], log_data["Title"], log_data["Description"]
        )

        # Step 6: Log time to Tempo
        return self.jira_manager.time_logger.log_time(selected_ticket["key"], log_data)
