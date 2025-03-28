import os
from pystray import Icon, Menu, MenuItem
from PIL import Image
from services.logger.log_manager import LogManager
from ui.views.settings import open_settings_window

class SystemTray:
    """System tray icon for WAID service with minimal options."""

    ICON_ACTIVE = os.path.join("ui/assets", "waid_active.png")
    ICON_INACTIVE = os.path.join("ui/assets", "waid_inactive.png")

    service_active = True
    icon = None

    @classmethod
    def toggle_service(cls, icon, item) -> None:
        """Toggle WAID service on/off."""
        cls.service_active = not cls.service_active
        cls.icon.icon = Image.open(cls.ICON_ACTIVE if cls.service_active else cls.ICON_INACTIVE)
        cls.update_menu()

        if cls.service_active:
            LogManager.start()
        else:
            LogManager.stop()

    @classmethod
    def open_settings(cls, icon, item) -> None:
        """Open the settings window."""
        open_settings_window()

    @classmethod
    def build_menu(cls) -> Menu:
        """Construct the system tray menu."""
        return Menu(
            MenuItem("Service Active", cls.toggle_service, checked=lambda item: cls.service_active),
            Menu.SEPARATOR,
            MenuItem("Settings", cls.open_settings)
        )

    @classmethod
    def update_menu(cls) -> None:
        """Update the menu dynamically."""
        cls.icon.menu = cls.build_menu()
        cls.icon.update_menu()

    @classmethod
    def start(cls) -> None:
        """Start the system tray icon."""
        cls.icon = Icon("WAID Service", Image.open(cls.ICON_ACTIVE), menu=cls.build_menu())
        cls.icon.run()
