import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Access to .env and get the value of SECRET_KEY
    JWT_SECRET_KEY =  os.environ.get("SECRET_KEY")
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Access to .env and get the value of DATABASE_URL
        value = os.environ.get("DATABASE_URL")

        if not value:
            raise ValueError("DATABASE_URL is not set")

        return value

# This app is currently in development, allowing for debugging while running in Flask
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

environment = os.environ.get("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()