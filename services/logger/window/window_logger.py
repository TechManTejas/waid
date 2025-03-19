from pynput import mouse
import Xlib
import Xlib.display
import subprocess
import json
import time
from services.logger.log_manager import LogManager

class WindowLogger:
    """Logs active window changes and user interactions with windows."""

    def __init__(self) -> None:
        self.display = Xlib.display.Display()
        self.root = self.display.screen().root
        self.active_window_title = None
        self.listener = mouse.Listener(on_click=self.on_click)

    def get_active_window_title(self) -> str:
        """Retrieve the title of the currently focused window."""
        try:
            output = subprocess.run(
                ["xdotool", "getwindowfocus", "getwindowname"], 
                capture_output=True, text=True
            )
            if output.returncode == 0:
                return output.stdout.strip()
        except Exception as e:
            LogManager.log(f"Error getting window title: {e}")
        return None

    def log_window_change(self) -> None:
        """Log when a new window becomes active."""
        window_title = self.get_active_window_title()

        if window_title and window_title != self.active_window_title:
            log_entry = {
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "window_title": window_title
            }
            LogManager.log(json.dumps(log_entry))
            self.active_window_title = window_title

    def on_click(self, x, y, button, pressed) -> None:
        """Detect user interaction and log window changes."""
        print("pressed", x, y, button, pressed)
        if pressed:
            self.log_window_change()

    def start(self) -> None:
        """Start the window logging process."""
        self.listener.start()

    def stop(self) -> None:
        """Stop the window logging process."""
        self.listener.stop()
