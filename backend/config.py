# ReWear Clothing System - Configuration
# Environment and application configuration settings

import os
from datetime import timedelta

class Config:
    """
    Base configuration class
    """
    DEBUG = False
    TESTING = False
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Sustainability constants
    CO2_PER_ITEM_KG = 3.0  # kg CO2 per item
    WATER_PER_ITEM_LITERS = 7000  # liters per item
    TEXTILE_WASTE_PER_ITEM_KG = 0.5  # kg per item


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///rewear.db'
    )
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Stricter settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)


class TestingConfig(Config):
    """
    Testing configuration
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
