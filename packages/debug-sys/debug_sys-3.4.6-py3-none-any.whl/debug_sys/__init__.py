#=============================== IMPORTS ZONE ===============================

#=============================== INIT ZONE ===============================
__version__ = "3.4.6"
__authors__ = ["CUISSET Mattéo"]
__license__ = "MIT"
__copyright__ = "Copyright 2022, CUISSET Mattéo"
__status__ = "dev"


#=============================== MAIN ZONE ===============================
from .logger import Logger
from .log_manager import LogManager

__all__ = ["Logger", "LogManager"]

class Types:
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class Levels:
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class Config:
    def __init__(self, log_dir: str, log_file: str, log_level: int, log_format: str, log_date_format: str):
        self.log_dir = log_dir
        self.log_file = log_file
        self.log_level = log_level
        self.log_format = log_format
        self.log_date_format = log_date_format

class DebugSys:
    def __init__(self, config: Config):
        self.config = config
        self.log_manager = LogManager(config)

    def log(self, message: str, level: int = Levels.INFO, type: str = Types.INFO):
        self.log_manager.log(message, level, type)

    def debug(self, message: str):
        self.log(message, Levels.DEBUG, Types.DEBUG)

    def info(self, message: str):
        self.log(message, Levels.INFO, Types.INFO)

    def warning(self, message: str):
        self.log(message, Levels.WARNING, Types.WARNING)

    def error(self, message: str):
        self.log(message, Levels.ERROR, Types.ERROR)
