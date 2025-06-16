import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    API_KEY = os.environ.get('API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    MODEL_NAME = os.environ.get('MODEL_NAME')
    FINE_TUNED_MODEL = os.environ.get('FINE_TUNED_MODEL', 'gpt-4o-mini')
    
    # Cache configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Rate limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Security headers
    CONTENT_SECURITY_POLICY = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval' https://stackpath.bootstrapcdn.com https://code.jquery.com https://cdn.jsdelivr.net",
        'style-src': "'self' 'unsafe-inline' https://stackpath.bootstrapcdn.com https://fonts.googleapis.com",
        'font-src': "'self' https://fonts.gstatic.com",
        'img-src': "'self' data:",
        'connect-src': "'self'"
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    CACHE_TYPE = 'simple'  # Change to 'redis' or 'memcached' in production
    
    # Stricter rate limiting in production
    RATELIMIT_DEFAULT = "100 per day"
    
    # Stricter security headers in production
    CONTENT_SECURITY_POLICY = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval' https://stackpath.bootstrapcdn.com https://code.jquery.com https://cdn.jsdelivr.net",
        'style-src': "'self' 'unsafe-inline' https://stackpath.bootstrapcdn.com https://fonts.googleapis.com",
        'font-src': "'self' https://fonts.gstatic.com",
        'img-src': "'self'",
        'connect-src': "'self'"
    }

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    CACHE_TYPE = 'null'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 