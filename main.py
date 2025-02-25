# import logging
# from waid.core.window_logger import WindowLogger
# from waid.core.log_summarizer import LogSummarizer
# from waid.ui.waid_tray import SystemTray
# from waid.utils.config import load_config

# def main():
#     # Initialize logging
#     logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
#     # Load configuration
#     config = load_config()

#     # Start window logger
#     logger = WindowLogger(config)
#     logger.start()

#     # Start summarization service
#     summarizer = LogSummarizer(config)
#     summarizer.run()

#     # Start system tray UI
#     tray = SystemTray()
#     tray.run()

# if __name__ == "__main__":
#     main()
