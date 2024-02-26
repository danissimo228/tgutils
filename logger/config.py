from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

SERVICE_NAME = os.getenv("SERVICE_NAME")

LOG_DIR = Path(__file__).resolve().parent.parent.parent.parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_colored': {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s %(name)-1s %(levelname)-1s %(message)s",
            "log_colors": {
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red",
            },
            "style": "%",
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_colored'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': LOG_DIR / f"{SERVICE_NAME}.log",
        }
    },
    'loggers': {
        'project.service': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'project.routers': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        '__main__': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
    }
}
