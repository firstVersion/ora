import os

from config import Config, ConfigValue


class OraConfig(Config):
    def __init__(self):
        config_path: str = os.path.expanduser("~/.ora")
        default: list = [
            ConfigValue(key="a", default="", pattern=".*"),
            ConfigValue(key="b", default="", pattern=".*"),
            ConfigValue(key="c", default="", pattern=".*"),
        ]
        super().__init__(config_path=config_path, default=default)
