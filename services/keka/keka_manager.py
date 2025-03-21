# keka_manager
# keka_manager

import requests
import datetime
import json
import logging
from typing import Dict, List, Optional, Union


class KekaManager:
    """
    A class to interact with qed42.keka.com API to retrieve leaves and holidays information.
    """

    def __init__(
        self,
        base_url: str = "https://qed42.keka.com/api",
        client_id: str = None,
        client_secret: str = None,
        username: str = None,
        password: str = None,
    ):
        """
        Initialize the KekaManager with necessary credentials.

        Args:
            base_url: The base URL for Keka API
            client_id: The client ID for API authentication
            client_secret: The client secret for API authentication
            username: Username for password grant authentication (if applicable)
            password: Password for password grant authentication (if applicable)
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = None
        self.token_expiry = None
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Setup logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def authenticate(self) -> bool:
        """
        Authenticate with the Keka API and get an access token.

        Returns:
            bool: True if authentication was successful, False otherwise
        """
        try:
            # This is a generic OAuth2 authentication implementation
            # You may need to adjust based on Keka's specific requirements
            auth_url = f"{self.base_url}/auth/token"

            # OAuth2 client credentials flow
            payload = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

            # If using password grant, use this payload instead
            # payload = {
            #    "grant_type": "password",
            #    "client_id": self.client_id,
            #    "client_secret": self.client_secret,
            #    "username": self.username,
            #    "password": self.password
            # }

            response = requests.post(auth_url, json=payload, headers=self.headers)

            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                expires_in = token_data.get("expires_in", 3600)  # Default 1 hour
                self.token_expiry = datetime.datetime.now() + datetime.timedelta(
                    seconds=expires_in
                )

                # Update headers with the access token
                self.headers["Authorization"] = f"Bearer {self.access_token}"
                self.logger.info("Successfully authenticated with Keka API")
                return True
            else:
                self.logger.error(
                    f"Authentication failed: {response.status_code} - {response.text}"
                )
                return False

        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            return False

    def _check_token_validity(self) -> bool:
        """
        Check if the current token is valid and refresh if needed.

        Returns:
            bool: True if a valid token is available, False otherwise
        """
        if not self.access_token:
            return self.authenticate()

        # Check if token is about to expire (within 5 minutes)
        if datetime.datetime.now() > (
            self.token_expiry - datetime.timedelta(minutes=5)
        ):
            return self.authenticate()

        return True

    def get_user_leaves(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict:
        """
        Get leaves for a user within the specified date range.

        Args:
            user_id: User ID (defaults to current user if None)
            start_date: Start date in YYYY-MM-DD format (defaults to beginning of current year)
            end_date: End date in YYYY-MM-DD format (defaults to end of current year)

        Returns:
            Dict containing leave information or error details
        """
        if not self._check_token_validity():
            return {"error": "Authentication failed"}

        try:
            # Set default date range to current year if not specified
            if not start_date:
                current_year = datetime.datetime.now().year
                start_date = f"{current_year}-01-01"

            if not end_date:
                current_year = datetime.datetime.now().year
                end_date = f"{current_year}-12-31"

            # Construct the API endpoint
            endpoint = f"{self.base_url}/leaves"

            # Prepare parameters
            params = {"startDate": start_date, "endDate": end_date}

            # Add user_id parameter if provided
            if user_id:
                params["userId"] = user_id

            # Make the API request
            response = requests.get(endpoint, headers=self.headers, params=params)

            if response.status_code == 200:
                leaves_data = response.json()
                self.logger.info(f"Successfully retrieved leaves data")
                return leaves_data
            else:
                error_msg = (
                    f"Failed to get leaves: {response.status_code} - {response.text}"
                )
                self.logger.error(error_msg)
                return {"error": error_msg}

        except Exception as e:
            error_msg = f"Error retrieving leaves: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}

    def get_leave_balance(self, user_id: Optional[str] = None) -> Dict:
        """
        Get leave balance for a user.

        Args:
            user_id: User ID (defaults to current user if None)

        Returns:
            Dict containing leave balance information or error details
        """
        if not self._check_token_validity():
            return {"error": "Authentication failed"}

        try:
            # Construct the API endpoint
            endpoint = f"{self.base_url}/leaves/balance"

            # Prepare parameters
            params = {}

            # Add user_id parameter if provided
            if user_id:
                params["userId"] = user_id

            # Make the API request
            response = requests.get(endpoint, headers=self.headers, params=params)

            if response.status_code == 200:
                balance_data = response.json()
                self.logger.info(f"Successfully retrieved leave balance data")
                return balance_data
            else:
                error_msg = f"Failed to get leave balance: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {"error": error_msg}

        except Exception as e:
            error_msg = f"Error retrieving leave balance: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}

    def get_holidays(self, year: Optional[int] = None) -> Dict:
        """
        Get holidays list for the specified year.

        Args:
            year: The year for which to fetch holidays (defaults to current year)

        Returns:
            Dict containing holiday information or error details
        """
        if not self._check_token_validity():
            return {"error": "Authentication failed"}

        try:
            # Use current year if not specified
            if not year:
                year = datetime.datetime.now().year

            # Construct the API endpoint
            endpoint = f"{self.base_url}/holidays"

            # Prepare parameters
            params = {"year": year}

            # Make the API request
            response = requests.get(endpoint, headers=self.headers, params=params)

            if response.status_code == 200:
                holidays_data = response.json()
                self.logger.info(f"Successfully retrieved holidays data for {year}")
                return holidays_data
            else:
                error_msg = (
                    f"Failed to get holidays: {response.status_code} - {response.text}"
                )
                self.logger.error(error_msg)
                return {"error": error_msg}

        except Exception as e:
            error_msg = f"Error retrieving holidays: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}

    def get_user_profile(self, user_id: Optional[str] = None) -> Dict:
        """
        Get user profile information.

        Args:
            user_id: User ID (defaults to current user if None)

        Returns:
            Dict containing user profile information or error details
        """
        if not self._check_token_validity():
            return {"error": "Authentication failed"}

        try:
            # Construct the API endpoint
            endpoint = f"{self.base_url}/employees/profile"

            # Prepare parameters
            params = {}

            # Add user_id parameter if provided
            if user_id:
                params["userId"] = user_id

            # Make the API request
            response = requests.get(endpoint, headers=self.headers, params=params)

            if response.status_code == 200:
                profile_data = response.json()
                self.logger.info(f"Successfully retrieved user profile data")
                return profile_data
            else:
                error_msg = f"Failed to get user profile: {response.status_code} - {response.text}"
                self.logger.error(error_msg)
                return {"error": error_msg}

        except Exception as e:
            error_msg = f"Error retrieving user profile: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}

    def save_config(self, config_path: str) -> bool:
        """
        Save API configuration to a file (without sensitive credentials).

        Args:
            config_path: Path to save the configuration file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create a configuration dictionary (excluding sensitive information)
            config = {
                "base_url": self.base_url,
                # Store only masked client_id for reference
                "client_id_mask": (
                    f"{self.client_id[:4]}****" if self.client_id else None
                ),
                # Don't store client_secret, username or password
            }

            with open(config_path, "w") as config_file:
                json.dump(config, config_file, indent=4)

            self.logger.info(f"Configuration saved to {config_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {str(e)}")
            return False
