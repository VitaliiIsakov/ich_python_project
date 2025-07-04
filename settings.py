"""
Settings module for database configurations.

Loads environment variables from .env file for MySQL and MongoDB connections.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MySQL settings
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = 3306
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

# MongoDB settings
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")