"""
Configuration Module
Manages application settings and environment variables
"""

import os
from pathlib import Path

class Config:
    """Base configuration"""
    
    # Application
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    
    # Paths
    BASE_DIR = Path(__file__).parent
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    PROCESSED_FOLDER = BASE_DIR / 'static' / 'processed'
    TEMP_FOLDER = BASE_DIR / 'static' / 'temp'
    MODEL_PATH = BASE_DIR / 'saved_models' / 'u2net' / 'u2net.pth'
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}
    MAX_BATCH_SIZE = 10
    
    # Model
    MODEL_INPUT_SIZE = 320
    
    # API
    API_RATE_LIMIT = '100 per hour'
    API_KEY_REQUIRED = os.environ.get('API_KEY_REQUIRED', 'False') == 'True'
    
    # Storage
    MAX_STORED_IMAGES = 100  # Maximum number of processed images to keep
    CLEANUP_AFTER_DAYS = 7  # Delete images older than this
    
    @classmethod
    def init_app(cls, app):
        """Initialize application with this config"""
        # Create required directories
        for folder in [cls.UPLOAD_FOLDER, cls.PROCESSED_FOLDER, cls.TEMP_FOLDER]:
            folder.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with environment variables in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError('SECRET_KEY environment variable must be set in production')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration by name"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])

