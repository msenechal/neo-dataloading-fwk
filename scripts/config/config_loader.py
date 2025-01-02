# Config loader for .env file or from the system env

from dotenv import load_dotenv
import os

# Load configuration from .env file
load_dotenv('.env')

# Load configuration from system env
URI = os.getenv('NEO4J_URI')
USERNAME = os.getenv('NEO4J_USERNAME')
PASSWORD = os.getenv('NEO4J_PASSWORD')

print(URI, USERNAME, PASSWORD)