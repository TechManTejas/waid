from pynput import mouse
import Xlib
import Xlib.display
import subprocess
import time
import json
import os

LOG_FILE = os.path.expanduser("~/waid.log")

class WindowLogger:
    def __init__(self):
        self.display = Xlib.display.Display()
        self.root = self.display.screen().root
        self.window_history = {}
        self.active_window_title = None
        self.window_counter = 1
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def get_active_window_title(self):
        try:
            output = subprocess.run(["xdotool", "getwindowfocus", "getwindowname"], capture_output=True, text=True)
            if output.returncode == 0:
                return output.stdout.strip()
        except Exception as e:
            self.log(f"Error getting window title: {e}")
        return None

    def log(self, message):
        """Write logs to a file."""
        with open(LOG_FILE, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def log_window_change(self):
        window_title = self.get_active_window_title()

        if window_title and window_title != self.active_window_title:
            timestamp = time.time()
            log_entry = {
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "window_title": window_title
            }
            self.log(json.dumps(log_entry))

            if window_title not in self.window_history:
                self.window_history[window_title] = {
                    "id": self.window_counter,
                    "start_time": timestamp,
                    "active_duration": 0,
                    "end_time": None
                }
                self.window_counter += 1
            else:
                self.window_history[window_title]["active_duration"] += time.time() - self.window_history[window_title]["start_time"]

            if self.active_window_title and self.active_window_title in self.window_history:
                self.window_history[self.active_window_title]["end_time"] = timestamp

            self.active_window_title = window_title

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.log_window_change()

if __name__ == "__main__":
    logger = WindowLogger()
    logger.listener.join()