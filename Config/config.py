import logging
import os

from colorama import init, Fore, Style
from dotenv import load_dotenv

# Initialize colorama for cross-platform color support
init()

# Custom formatter with colors
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"

# Load environment variables from .env file
load_dotenv()

# Configure logging
formatter = ColoredFormatter(
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Handlers
file_handler = logging.FileHandler("../Logs/selenium.log")
file_handler.setFormatter(logging.Formatter(  # Plain formatter for file (no colors)
    fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,  # Adjust to DEBUG for more detail
    handlers=[file_handler, console_handler]
)

class Config:
    # Retrieve credentials from environment variables
    TRT_USERNAME = os.getenv("TRT_USERNAME")
    TMS_USERNAME = os.getenv("TMS_USERNAME")
    LABGATE_USERNAME = os.getenv("LABGATE_USERNAME")
    PASSWORD = os.getenv("PASSWORD")

    TMS_COMMON_USERNAME = os.getenv("TMS_COMMON_USERNAME")
    TMS_COMMON_PASSWORD = os.getenv("TMS_COMMON_PASSWORD")
    TMS_REPOSITORY = os.getenv("TMS_REPOSITORY")

    TRT_URL = os.getenv("TRT_URL")
    TMS_URL = os.getenv("TMS_URL")
    LABGATE_URL = os.getenv("LABGATE_URL")


    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

    @staticmethod
    def validate():
        logger = logging.getLogger(__name__)
        if not Config.TRT_USERNAME:
            logger.error("TRT_USERNAME is not set in the environment variables.")
            raise ValueError("TRT_USERNAME is not set in the environment variables.")
        if not Config.TMS_USERNAME:
            logger.error("TMS_USERNAME is not set in the environment variables.")
            raise ValueError("TMS_USERNAME is not set in the environment variables.")
        if not Config.LABGATE_USERNAME:
            logger.error("LABGATE_USERNAME is not set in the environment variables.")
            raise ValueError("LABGATE_USERNAME is not set in the environment variables.")
        if not Config.PASSWORD:
            logger.error("PASSWORD is not set in the environment variables.")
            raise ValueError("PASSWORD is not set in the environment variables.")
        if not Config.TMS_COMMON_USERNAME:
            logger.error("TMS_COMMON_USERNAME is not set in the environment variables.")
            raise ValueError("TMS_COMMON_USERNAME is not set in the environment variables.")
        if not Config.TMS_COMMON_PASSWORD:
            logger.error("TMS_COMMON_PASSWORD is not set in the environment variables.")
            raise ValueError("TMS_COMMON_PASSWORD is not set in the environment variables.")
        if not Config.TMS_REPOSITORY:
            logger.error("TMS_REPOSITORY is not set in the environment variables.")
            raise ValueError("TMS_REPOSITORY is not set in the environment variables.")
        if not Config.TRT_URL:
            logger.error("TRT_URL is not set in the environment variables.")
            raise ValueError("TRT_URL is not set in the environment variables.")
        if not Config.TMS_URL:
            logger.error("TMS_URL is not set in the environment variables.")
            raise ValueError("TMS_URL is not set in the environment variables.")
        if not Config.LABGATE_URL:
            logger.error("LABGATE_URL is not set in the environment variables.")
            raise ValueError("LABGATE_URL is not set in the environment variables.")
        if not Config.CHROMEDRIVER_PATH:
            logger.error("You need to set the path to the chromedriver executable in the environment variables")
            raise ValueError("You need to set the path to the chromedriver executable in the environment variables")
        logger.info("All required environment variables are set.")