from pystray import Icon, Menu, MenuItem
from PIL import Image

# Paths to icons
ICON_ACTIVE = "assets/waid_active.png"
ICON_INACTIVE = "assets/waid_inactive.png"

# Load images for system tray
image_active = Image.open(ICON_ACTIVE)
image_inactive = Image.open(ICON_INACTIVE)

# Global variables
service_active = True
sensitivity = 50

def toggle_service(icon, item):
    """Toggle WAID service on/off."""
    global service_active
    service_active = not service_active
    icon.icon = image_active if service_active else image_inactive
    icon.update_menu()

def set_sensitivity(icon, item, value):
    """Set sensitivity level."""
    global sensitivity
    sensitivity = value
    icon.update_menu()

# Define sensitivity submenu directly inside MenuItem
sensitivity_menu = MenuItem(
    "Sensitivity",
    Menu(
        MenuItem("Low (25%)", lambda icon, item: set_sensitivity(icon, item, 25), checked=lambda item: sensitivity == 25),
        MenuItem("Medium (50%)", lambda icon, item: set_sensitivity(icon, item, 50), checked=lambda item: sensitivity == 50),
        MenuItem("High (75%)", lambda icon, item: set_sensitivity(icon, item, 75), checked=lambda item: sensitivity == 75),
    )
)

# Define the main menu
menu = Menu(
    MenuItem("Service Active", toggle_service, checked=lambda item: service_active),
    Menu.SEPARATOR,
    sensitivity_menu,  # Directly include the submenu
    Menu.SEPARATOR,
    MenuItem("Settings (Placeholder)", lambda icon, item: print("Opening Settings...")),
)

# Initialize and run the system tray icon
icon = Icon("WAID Service", image_active, menu=menu)
icon.run()
