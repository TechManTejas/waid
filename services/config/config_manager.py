import json
import os
import threading

class ConfigManager:
    """Manages reading, writing, and modifying config.json dynamically."""

    CONFIG_PATH = os.path.expanduser("~/waid/config.json") 
    _lock = threading.Lock()
    _default_config = {}

    @classmethod
    def _ensure_config_exists(cls):
        """Ensure config.json exists with default values if missing."""
        if not os.path.exists(cls.CONFIG_PATH):
            os.makedirs(os.path.dirname(cls.CONFIG_PATH), exist_ok=True)
            cls._save_config(cls._default_config)

    @classmethod
    def _load_config(cls) -> dict:
        """Load the configuration from config.json."""
        cls._ensure_config_exists()
        with cls._lock, open(cls.CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _save_config(cls, new_config: dict) -> bool:
        """Save the updated configuration to config.json."""
        try:
            with cls._lock, open(cls.CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(new_config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    @classmethod
    def get(cls, key: str):
        """Get a value from config.json by key."""
        config = cls._load_config()
        return config.get(key, None)  

    @classmethod
    def set(cls, key: str, value) -> bool:
        """Set a key-value pair in config.json."""
        config = cls._load_config()
        config[key] = value  
        return cls._save_config(config)
