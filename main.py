from services.startup.startup_manager import StartupManager
from ui.system_tray import SystemTray

def main() -> None:
    """Entry point for the application."""
    StartupManager.run() 

    tray = SystemTray()
    tray.start()

if __name__ == "__main__":
    main()
