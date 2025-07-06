# config.py
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "curriculos")

    # Configurações do Flask-Smorest
    API_TITLE = "MyClass API"
    API_VERSION = "1.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_JSON_PATH = "/openapi.json"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    OPENAPI_URL_PREFIX = ""


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    CORS_ORIGINS = "*"
    PORT = 5000


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    CORS_ORIGINS = "https://seu-front.com"
    PORT = 80
