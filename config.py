from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
try:
    DATABASE_URL = os.getenv("DATABASE_URL")
except Exception as e:
    print(f"Error loading environment variables: {e}")
    DATABASE_URL = None