"""Default configuration

Use env var to override
"""
import os

SERVER_NAME = os.getenv("SERVER_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
# URL scheme to use outside of request context
# do not configure as https unless reverse proxy secured
PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", 'http')
