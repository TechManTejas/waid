import subprocess

class Notification:
    """Handles system notifications for the WAID service."""

    @classmethod
    def send(cls, message: str) -> None:
        """
        Send a system notification with the given message.

        :param message: The message to display in the notification.
        """
        subprocess.run(["notify-send", "WAID", message])
