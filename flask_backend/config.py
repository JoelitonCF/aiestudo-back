# config.py

# config.py
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "curriculos")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    CORS_ORIGINS = "*"         # ou "http://localhost:3000"
    PORT = 5000


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    CORS_ORIGINS = "https://seu-front.com"
    PORT = 80
