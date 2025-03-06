from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Set proper production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

# Dictionary to easily access different configs
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}