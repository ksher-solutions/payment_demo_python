from logging import DEBUG
import os
from dotenv import load_dotenv

class Config:
    """Basic Flask configuration.
    """
    load_dotenv()

    DEBUG=True
    KSHER_API_TOKEN = os.environ["KSHER_API_TOKEN"]
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]

    KSHER_API_BASE = os.environ.get("KSHER_API_BASE", "https://dev.vip.ksher.net")
    
    STORE_LOCALE = os.environ.get("STORE_LOCALE", "th_TH")
    STORE_CURRENCY = os.environ.get("STORE_CURRENCY", "THB")
    SERVER_NAME = os.environ.get("SERVER_NAME")
    AUTO_CAPTURE = os.environ.get("AUTO_CAPTURE") not in [0, "false", "False"]
    LOCATION = os.environ.get("LOCATION") not in [0, "false", "False"]
    STORE_BASE_URL = os.environ.get("STORE_BASE_URL", "http://localhost:5000")
