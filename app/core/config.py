import os
import logging
from termcolor import colored
from dotenv import load_dotenv

load_dotenv()

"""
# Logger
"""
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'magenta',
    }

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname, 'white'))

def setup_logger():
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s: %(message)s'))

    logger.addHandler(console_handler)
    return logger

logger = setup_logger()

"""
# Security
"""
PUBLIC_KEY = os.getenv("PUBLIC_KEY", "your_public_key_here")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")
"""
# Image Processing
"""
IMAGE_QUALITY = os.getenv("IMAGE_QUALITY", "75")
IMAGE_FORMAT = os.getenv("IMAGE_FORMAT", "WEBP")
IMAGE_SUPPORTED_FORMATS = os.getenv("IMAGE_SUPPORTED_FORMATS",
                                    {"JPEG", "JPG", "PNG", "WEBP", "AVIF", "GIF", "TIFF", "BMP", "HEIC"})

"""
# Utils
"""
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/var/www/uploads")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
