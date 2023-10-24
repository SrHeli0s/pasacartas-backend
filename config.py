import os

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    POSTGRES_URL=os.environ.get('POSTGRES_URL')
    POSTGRES_USER=os.environ.get('POSTGRES_USER')
    POSTGRES_HOST=os.environ.get('POSTGRES_HOST')
    POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DATABASE=os.environ.get('POSTGRES_DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
}