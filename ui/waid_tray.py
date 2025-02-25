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
sensitivity_levels = [25, 50, 75]  # Default sensitivity levels

def toggle_service(icon, item):
    """Toggle WAID service on/off."""
    global service_active
    service_active = not service_active
    icon.icon = image_active if service_active else image_inactive
    update_menu(icon)  # Update menu dynamically

def set_sensitivity(icon, item, value):
    """Set sensitivity level and update menu dynamically."""
    global sensitivity
    sensitivity = value
    update_menu(icon)

def add_sensitivity_level(icon, item):
    """Dynamically add a new sensitivity level at runtime."""
    global sensitivity_levels
    new_level = max(sensitivity_levels) + 10  # Example: Add 10% more than max
    sensitivity_levels.append(new_level)
    update_menu(icon)

def sensitivity_item(level):
    """Return a menu item for a given sensitivity level."""
    return MenuItem(
        f"{level}%",
        lambda icon, item: set_sensitivity(icon, item, level),
        checked=lambda item: sensitivity == level
    )

def build_sensitivity_menu():
    """Dynamically build the sensitivity submenu."""
    return Menu(
        *[sensitivity_item(level) for level in sensitivity_levels],  # Generate menu items properly
        Menu.SEPARATOR,
        MenuItem("Add Custom Level", add_sensitivity_level)  # Allows adding new levels dynamically
    )

def update_menu(icon):
    """Rebuild and update the menu dynamically."""
    icon.menu = Menu(
        MenuItem("Service Active", toggle_service, checked=lambda item: service_active),
        Menu.SEPARATOR,
        MenuItem("Sensitivity", build_sensitivity_menu()),  # Dynamic submenu
        Menu.SEPARATOR,
        MenuItem("Settings (Placeholder)", lambda icon, item: print("Opening Settings...")),
    )
    icon.update_menu()

# Initialize the system tray icon
icon = Icon("WAID Service", image_active)
update_menu(icon)  # Set initial menu
icon.run()
