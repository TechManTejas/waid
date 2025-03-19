from ui.system_tray import SystemTray

def main() -> None:
    """Entry point for the application, responsible for launching the system tray."""
    tray = SystemTray()
    tray.start()

if __name__ == "__main__":
    main()
