from pystray import Icon, Menu, MenuItem
from PIL import Image
import os
from services.logger.log_manager import LogManager

class SystemTray:
    """System tray icon for WAID service with minimal options."""

    ICON_ACTIVE = os.path.join("ui/assets", "waid_active.png")
    ICON_INACTIVE = os.path.join("ui/assets", "waid_inactive.png")

    def __init__(self) -> None:
        self.image_active = Image.open(self.ICON_ACTIVE)
        self.image_inactive = Image.open(self.ICON_INACTIVE)
        self.service_active = True
        self.icon = Icon("WAID Service", self.image_active, menu=self.build_menu())
        
        # Initialize Log Manager
        self.log_manager = LogManager()
        self.log_manager.start()

    def toggle_service(self, icon, item) -> None:
        """Toggle WAID service on/off."""
        self.service_active = not self.service_active
        self.icon.icon = self.image_active if self.service_active else self.image_inactive
        self.update_menu()

        # Start or stop logging based on service state
        if self.service_active:
            self.log_manager.start()
        else:
            self.log_manager.stop()

    def open_settings(self, icon, item) -> None:
        """Placeholder for opening settings."""
        print("Opening Settings...")

    def build_menu(self) -> Menu:
        """Construct the system tray menu."""
        return Menu(
            MenuItem("Service Active", self.toggle_service, checked=lambda item: self.service_active),
            Menu.SEPARATOR,
            MenuItem("Settings", self.open_settings)
        )

    def update_menu(self) -> None:
        """Update the menu dynamically."""
        self.icon.menu = self.build_menu()
        self.icon.update_menu()

    def start(self) -> None:
        """Start the system tray icon."""
        self.icon.run()
