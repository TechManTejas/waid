from PyQt6.QtWidgets import QApplication, QWidget
import sys

app = None

def open_settings_window():
    """Open a blank settings window."""
    global app

    if app is None:
        app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Settings")
    window.resize(800, 600)

    window.show()

    app.exec()
