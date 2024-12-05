"""This module define project configurations variables"""

from decouple import config

# -- API Constants --
API_TOKEN = config("MINDSIGHT_AUTH_API_TOKEN", default=None)
API_COMPANY = config("MINDSIGHT_AUTH_API_COMPANY", default=None)
API_SERVER = config("MINDSIGHT_AUTH_API_SERVER", default=None)
API_VERSION = config("MINDSIGHT_AUTH_API_VERSION", default="v1")

# Request config
PAGE_SIZE: int = 1000
TIMEOUT: int = 600  # Default set to 600 seconds (10 minutes)

# Date formats
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATE_FORMAT = "%Y-%m-%d"

# Endpoints
API_ENDPOINT_USERS = "/users"
