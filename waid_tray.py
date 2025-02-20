import gi
import time
import threading

gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import AppIndicator3, Gtk, GLib
import os
import subprocess

ICON_ACTIVE = os.path.abspath("waid_active.png")
ICON_INACTIVE = os.path.abspath("waid_inactive.png")
ICON_PAUSED = os.path.abspath("waid_paused.png")
LOG_FILE = os.path.expanduser("~/waid.log")

timer_running = False
start_time = None

def notify(message):
    subprocess.run(["notify-send", "WAID Service", message])

def open_log_file(_):
    subprocess.run(["xdg-open", LOG_FILE])

def update_timer():
    while timer_running:
        if start_time:
            elapsed = int(time.time() - start_time)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            GLib.idle_add(indicator.set_label, f"Add 2-3 Fields in Theme Settings... {hours:02}:{minutes:02}:{seconds:02}", "WAID Timer")
        time.sleep(1)

def start_timer():
    global timer_running, start_time
    timer_running = True
    start_time = time.time()
    threading.Thread(target=update_timer, daemon=True).start()

def stop_timer():
    global timer_running
    timer_running = False
    GLib.idle_add(indicator.set_label, "WAID", "WAID Timer")

def set_icon(icon_name):
    indicator.set_icon_full(icon_name, "")

def set_active(_):
    notify("WAID Service Active")
    set_icon(ICON_ACTIVE)
    start_timer()

def set_inactive(_):
    notify("WAID Service Inactive")
    set_icon(ICON_INACTIVE)
    stop_timer()

def set_paused(_):
    notify("WAID Service Paused")
    set_icon(ICON_PAUSED)
    stop_timer()

def quit_app(_):
    notify("Exiting WAID Tray.")
    stop_timer()
    Gtk.main_quit()

def open_settings_window(_):
    window = Gtk.Window(title="WAID Settings")
    window.set_default_size(400, 400)
    notebook = Gtk.Notebook()
    
    # General Settings Tab
    vbox_general = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    label = Gtk.Label(label="Enter custom setting:")
    vbox_general.pack_start(label, False, False, 0)
    entry = Gtk.Entry()
    vbox_general.pack_start(entry, False, False, 0)
    check_button = Gtk.CheckButton(label="Enable Feature")
    vbox_general.pack_start(check_button, False, False, 0)
    notebook.append_page(vbox_general, Gtk.Label(label="General"))
    
    # Advanced Settings Tab
    vbox_advanced = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    radio1 = Gtk.RadioButton.new_with_label_from_widget(None, "Option 1")
    radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Option 2")
    vbox_advanced.pack_start(radio1, False, False, 0)
    vbox_advanced.pack_start(radio2, False, False, 0)
    slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
    slider.set_range(0, 100)
    slider.set_value(50)
    vbox_advanced.pack_start(slider, False, False, 0)
    combo = Gtk.ComboBoxText()
    for item in ["Choice 1", "Choice 2", "Choice 3"]:
        combo.append_text(item)
    combo.set_active(0)
    vbox_advanced.pack_start(combo, False, False, 0)
    notebook.append_page(vbox_advanced, Gtk.Label(label="Advanced"))
    
    # Controls Tab
    vbox_controls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    spin_button = Gtk.SpinButton()
    spin_button.set_range(0, 100)
    spin_button.set_increments(1, 10)
    vbox_controls.pack_start(spin_button, False, False, 0)
    progress_bar = Gtk.ProgressBar()
    progress_bar.set_fraction(0.5)
    vbox_controls.pack_start(progress_bar, False, False, 0)
    button1 = Gtk.Button(label="Save Settings")
    button1.connect("clicked", lambda _: notify(f"Settings saved: {entry.get_text()}"))
    vbox_controls.pack_start(button1, False, False, 0)
    button2 = Gtk.Button(label="Close")
    button2.connect("clicked", lambda _: window.destroy())
    vbox_controls.pack_start(button2, False, False, 0)
    notebook.append_page(vbox_controls, Gtk.Label(label="Controls"))
    
    window.add(notebook)
    window.show_all()

def main():
    global indicator
    indicator = AppIndicator3.Indicator.new(
        "WAID Service",
        ICON_INACTIVE,
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    menu = Gtk.Menu()
    
    active_item = Gtk.MenuItem(label="Set Active")
    active_item.connect("activate", set_active)
    menu.append(active_item)
    
    inactive_item = Gtk.MenuItem(label="Set Inactive")
    inactive_item.connect("activate", set_inactive)
    menu.append(inactive_item)
    
    paused_item = Gtk.MenuItem(label="Set Paused")
    paused_item.connect("activate", set_paused)
    menu.append(paused_item)
    
    log_file_item = Gtk.MenuItem(label="Open Log File")
    log_file_item.connect("activate", open_log_file)
    menu.append(log_file_item)
    
    settings_item = Gtk.MenuItem(label="Settings")
    settings_item.connect("activate", open_settings_window)
    menu.append(settings_item)
    
    quit_item = Gtk.MenuItem(label="Quit")
    quit_item.connect("activate", quit_app)
    menu.append(quit_item)
    
    menu.show_all()
    indicator.set_menu(menu)
    Gtk.main()

if __name__ == "__main__":
    main()
