# config_selenium.py

import os

from dotenv import load_dotenv



class SeleniumConfig:
    """Configuration class for Immoware API operations."""

    # Load environment variables from .env file
    load_dotenv()

    MANDANT = os.getenv("IMMOWARE24_MANDANT")
    USERNAME = os.getenv("IMMOWARE24_USERNAME")
    PASSWORD = os.getenv("IMMOWARE24_PASSWORD")
    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
    DOWNLOAD_DIR = os.getenv("IMMOWARE24_DOWNLOAD_DIR")
