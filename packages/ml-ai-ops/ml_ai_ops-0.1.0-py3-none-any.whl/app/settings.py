"""
    This is a constants file where we define all the configs, constant variable, etc...
"""
import logging
import logging.config
import os
from dotenv import load_dotenv

load_dotenv(".config")

# Logging config
LOGGER_CONFIG= "logging.conf"

logging.config.fileConfig(LOGGER_CONFIG, disable_existing_loggers=False)

logging.getLogger("httpcore.http11").setLevel(logging.INFO)
logging.getLogger("httpcore.connection").setLevel(logging.INFO)
logging.getLogger("chromadb.config").setLevel(logging.INFO)
logging.getLogger("openai").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logging.getLogger("backoff").setLevel(logging.ERROR)
logging.getLogger("watchfiles.main").setLevel(logging.INFO)

# App config
APP_NAME = os.environ.get("APP_NAME", "zmp-aiops-backend")
APP_ROOT = os.environ.get("APP_ROOT", "/api/aiops/v1")
DOCS_URL = os.environ.get("DOCS_URL", f"{APP_ROOT}/api-docs")
REDOC_URL = os.environ.get("REDOC_URL", f"{APP_ROOT}/api-redoc")
OPENAPI_URL = os.environ.get("OPENAPI_URL", f"{APP_ROOT}/openapi")
APP_TITLE = os.environ.get("APP_TITLE", "AI-Ops Backend")
APP_VERSION = os.environ.get("APP_VERSION") # set by helm chart automatically
APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", "AI-Ops Backend API")


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")