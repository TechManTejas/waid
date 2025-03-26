import keyring
import keyring.errors

class SecretManager:
    """A secure secret manager using the system keyring for WAID."""

    SERVICE_NAME = "waid"

    @classmethod
    def set_secret(cls, key: str, value: str) -> bool:
        """
        Store a secret securely.

        :param key: The key (identifier) for the secret.
        :param value: The secret value to store.
        :return: True if successful, False otherwise.
        """
        try:
            keyring.set_password(cls.SERVICE_NAME, key, value)
            return True
        except keyring.errors.KeyringError as e:
            print(f"Error storing secret: {e}")
            return False

    @classmethod
    def get_secret(cls, key: str) -> str | None:
        """
        Retrieve a stored secret securely.

        :param key: The key (identifier) for the secret.
        :return: The stored secret, or None if not found.
        """
        try:
            return keyring.get_password(cls.SERVICE_NAME, key)
        except keyring.errors.KeyringError as e:
            print(f"Error retrieving secret: {e}")
            return None

    @classmethod
    def delete_secret(cls, key: str) -> bool:
        """
        Delete a stored secret securely.

        :param key: The key (identifier) for the secret.
        :return: True if successful, False otherwise.
        """
        try:
            keyring.delete_password(cls.SERVICE_NAME, key)
            return True
        except keyring.errors.PasswordDeleteError:
            print(f"Secret '{key}' not found.")
            return False
        except keyring.errors.KeyringError as e:
            print(f"Error deleting secret: {e}")
            return False

    @classmethod
    def secret_exists(cls, key: str) -> bool:
        """
        Check if a secret exists in the keyring.

        :param key: The key (identifier) for the secret.
        :return: True if the secret exists, False otherwise.
        """
        return cls.get_secret(key) is not None