import gi
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import AppIndicator3, Gtk
import os
import subprocess
from PIL import Image

ICON_RUNNING = os.path.expanduser("~/.waid_running.png")
ICON_STOPPED = os.path.expanduser("~/.waid_stopped.png")
LOG_FILE = os.path.expanduser("~/waid.log")

# Create icons dynamically
def create_icons():
    img_running = Image.new('RGB', (64, 64), (0, 255, 0))  # Green icon for running
    img_stopped = Image.new('RGB', (64, 64), (255, 0, 0))  # Red icon for stopped
    img_running.save(ICON_RUNNING)
    img_stopped.save(ICON_STOPPED)

# Show system notification
def notify(message):
    subprocess.run(["notify-send", "--icon=" + ICON_RUNNING, "WAID Service", message])

# Open log file
def open_log_file(_):
    subprocess.run(["xdg-open", LOG_FILE])

# Toggle logging (Checkable menu item)
def toggle_logging(menu_item):
    if menu_item.get_active():
        notify("Logging Enabled")
    else:
        notify("Logging Disabled")

# Change log level (Radio menu items)
def set_log_level(menu_item, level):
    if menu_item.get_active():
        notify(f"Log Level set to {level}")

# Stop WAID Service
def stop_waid(_):
    notify("Stopping WAID Service...")
    indicator.set_icon(ICON_STOPPED)

# Quit App
def quit_app(_):
    notify("Exiting WAID Tray.")
    Gtk.main_quit()

# Open a new window with buttons, text boxes, and labels
def open_settings_window(_):
    window = Gtk.Window(title="WAID Settings")
    window.set_default_size(300, 200)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox.set_margin_top(10)
    vbox.set_margin_bottom(10)
    vbox.set_margin_start(10)
    vbox.set_margin_end(10)
    
    # Label
    label = Gtk.Label(label="Enter custom setting:")
    vbox.pack_start(label, False, False, 0)

    # Text Entry Box
    entry = Gtk.Entry()
    vbox.pack_start(entry, False, False, 0)

    # Buttons
    button1 = Gtk.Button(label="Save Settings")
    button1.connect("clicked", lambda _: notify(f"Settings saved: {entry.get_text()}"))
    vbox.pack_start(button1, False, False, 0)

    button2 = Gtk.Button(label="Close")
    button2.connect("clicked", lambda _: window.destroy())
    vbox.pack_start(button2, False, False, 0)

    window.add(vbox)
    window.show_all()

# Create an AppIndicator3 system tray icon
def main():
    create_icons()

    global indicator
    indicator = AppIndicator3.Indicator.new(
        "WAID Service",
        ICON_RUNNING,
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    # Create menu
    menu = Gtk.Menu()

    # Stop WAID
    stop_item = Gtk.MenuItem(label="Stop WAID")
    stop_item.connect("activate", stop_waid)
    menu.append(stop_item)

    # Logging Toggle
    log_toggle = Gtk.CheckMenuItem(label="Enable Logging")
    log_toggle.set_active(True)
    log_toggle.connect("toggled", toggle_logging)
    menu.append(log_toggle)

    # Log Level (Radio Buttons)
    log_level_menu = Gtk.Menu()
    levels = ["Debug", "Info", "Warning", "Error"]
    group = None

    for level in levels:
        menu_item = Gtk.RadioMenuItem(label=level, group=group)
        group = menu_item
        menu_item.connect("toggled", set_log_level, level)
        log_level_menu.append(menu_item)

    log_level_item = Gtk.MenuItem(label="Log Level")
    log_level_item.set_submenu(log_level_menu)
    menu.append(log_level_item)

    # Open Log File
    log_file_item = Gtk.MenuItem(label="Open Log File")
    log_file_item.connect("activate", open_log_file)
    menu.append(log_file_item)

    # Open Settings Window
    settings_item = Gtk.MenuItem(label="Settings")
    settings_item.connect("activate", open_settings_window)
    menu.append(settings_item)

    # Quit App
    quit_item = Gtk.MenuItem(label="Quit")
    quit_item.connect("activate", quit_app)
    menu.append(quit_item)

    menu.show_all()
    indicator.set_menu(menu)

    Gtk.main()

if __name__ == "__main__":
    main()
