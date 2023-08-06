import logging
from colorama import Fore


class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        level = record.levelname
        if level == "DEBUG":
            level_color = Fore.GREEN + level + Fore.RESET
        elif level == "INFO":
            level_color = Fore.BLUE + level + Fore.RESET
        elif level == "WARNING":
            level_color = Fore.YELLOW + level + Fore.RESET
        elif level == "ERROR":
            level_color = Fore.RED + level + Fore.RESET
        elif level == "CRITICAL":
            level_color = Fore.MAGENTA + level + Fore.RESET
        else:
            level_color = level

        log_time = self.formatTime(record, self.datefmt)
        message = record.getMessage()
        return f"{log_time} {level_color} {message}"

log_name = "taskhub"
logger = logging.getLogger(log_name)

formatter = ColoredFormatter("%(asctime)s-%(levelname)s-%(message)s")

file_handler = logging.FileHandler(f"/var/log/{log_name}.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.setLevel(logging.INFO)
