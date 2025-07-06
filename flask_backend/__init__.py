import os
import logging
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_smorest import Api
from marshmallow import ValidationError

from .config import DevelopmentConfig, ProductionConfig
from .routes.flashcard import flashcard_bp
from .routes.curriculo import curriculo_bp
from .routes.desafio import desafio_bp
from .routes.plano import plano_bp
from .routes.quiz import quiz_bp
from .routes.user import user_bp
# from .routes.test_route import test_bp  # Removido pois o arquivo não existe mais


def configure_app(app):
    env = os.getenv("FLASK_ENV", "development").lower()
    cfg = ProductionConfig if env == "production" else DevelopmentConfig
    app.config.from_object(cfg)
    app.config.update({
        "API_TITLE": "MyClass API",
        "API_VERSION": "1.0",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_JSON_PATH": "/openapi.json",
        "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        "OPENAPI_URL_PREFIX": "/"
    })


def configure_logging(app):
    level = logging.DEBUG if app.debug or app.testing else logging.INFO
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    ))
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(level)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"erro": "Requisição inválida"}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Recurso não encontrado"}), 404

    @app.errorhandler(ValidationError)
    def handle_validation(err):
        return jsonify({"erros": err.messages}), 400

    @app.errorhandler(Exception)
    def internal_error(e):
        app.logger.exception(e)
        return jsonify({"erro": "Erro interno de servidor"}), 500


def register_extensions(app):
    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))


def register_blueprints(api):
    api.register_blueprint(flashcard_bp)
    api.register_blueprint(curriculo_bp)
    api.register_blueprint(desafio_bp)
    api.register_blueprint(plano_bp)
    api.register_blueprint(quiz_bp)
    api.register_blueprint(user_bp)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    configure_app(app)
    configure_logging(app)
    register_extensions(app)
    register_error_handlers(app)

    # inicializa flask-smorest
    api = Api(app)
    register_blueprints(api)

    # redireciona /swagger-ui → /swagger-ui/
    @app.route("/swagger-ui")
    def swagger_ui_redirect():
        return redirect("/swagger-ui/")

    return app
