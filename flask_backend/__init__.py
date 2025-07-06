# # Substitua seu __init__.py por este código corrigido

# import os
# import logging
# from flask import Flask, jsonify, redirect
# from flask_cors import CORS
# from flask_smorest import Api
# from marshmallow import ValidationError

# from .config import DevelopmentConfig, ProductionConfig
# from .routes.flashcard import flashcard_bp
# from .routes.curriculo import curriculo_bp
# from .routes.desafio import desafio_bp
# from .routes.plano import plano_bp
# from .routes.quiz import quiz_bp
# from .routes.user import user_bp


# def configure_app(app):
#     env = os.getenv("FLASK_ENV", "development").lower()
#     cfg = ProductionConfig if env == "production" else DevelopmentConfig
#     app.config.from_object(cfg)

#     # Configuração do Flask-Smorest
#     app.config.update({
#         "API_TITLE": "MyClass API",
#         "API_VERSION": "1.0",
#         "OPENAPI_VERSION": "3.0.3",
#         "OPENAPI_JSON_PATH": "/openapi.json",
#         "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
#         "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
#         # "OPENAPI_URL_PREFIX": "",
#         # Configurações adicionais para corrigir o problema
#         "OPENAPI_SWAGGER_UI_CONFIG": {
#             "deepLinking": True,
#             "displayOperationId": True,
#             "defaultModelsExpandDepth": 2,
#             "defaultModelExpandDepth": 2,
#             "displayRequestDuration": True,
#             "showExtensions": True,
#             "showCommonExtensions": True,
#         }
#     })


# def configure_logging(app):
#     level = logging.DEBUG if app.debug or app.testing else logging.INFO
#     handler = logging.StreamHandler()
#     handler.setFormatter(logging.Formatter(
#         "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
#     ))
#     app.logger.handlers.clear()
#     app.logger.addHandler(handler)
#     app.logger.setLevel(level)


# def register_error_handlers(app):
#     @app.errorhandler(400)
#     def bad_request(e):
#         return jsonify({"erro": "Requisição inválida"}), 400

#     @app.errorhandler(ValidationError)
#     def handle_validation(err):
#         return jsonify({"erros": err.messages}), 400

#     @app.errorhandler(Exception)
#     def internal_error(e):
#         app.logger.exception(e)
#         return jsonify({"erro": "Erro interno de servidor"}), 500

#     # NÃO registrar handler para 404 - deixa o Flask-Smorest gerenciar
#     # O handler 404 estava interceptando as rotas do Swagger UI


# def register_extensions(app):
#     CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))


# def register_blueprints(api):
#     api.register_blueprint(flashcard_bp)
#     api.register_blueprint(curriculo_bp)
#     api.register_blueprint(desafio_bp)
#     api.register_blueprint(plano_bp)
#     api.register_blueprint(quiz_bp)
#     api.register_blueprint(user_bp)


# def create_app():
#     app = Flask(__name__, instance_relative_config=False)

#     # Configurar app
#     configure_app(app)
#     configure_logging(app)
#     register_extensions(app)

#     # Inicializar API
#     api = Api(app)

#     # Registrar blueprints
#     register_blueprints(api)

#     # Registrar error handlers (sem o 404 que interfere com Swagger)
#     register_error_handlers(app)

#     # Rotas adicionais para debug
#     @app.route("/")
#     def index():
#         return {"message": "API funcionando!", "swagger": "/swagger-ui"}

#     @app.route("/debug")
#     def debug():
#         return {
#             "blueprints": [bp.name for bp in app.blueprints.values()],
#             "routes": [str(rule) for rule in app.url_map.iter_rules()],
#             "config": {k: v for k, v in app.config.items() if k.startswith("OPENAPI") or k.startswith("API")}
#         }

#     # Redirecionar para swagger-ui com barra
#     @app.route("/swagger-ui")
#     def swagger_ui_redirect():
#         return redirect("/swagger-ui/", code=301)

#     # Log das rotas registradas
#     app.logger.info("=== ROTAS REGISTRADAS ===")
#     for rule in app.url_map.iter_rules():
#         app.logger.info(f"{rule.methods} {rule.rule}")

#     return app

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


def configure_app(app: Flask):
    """Carrega config de ambiente e OpenAPI/Swagger."""
    env = os.getenv("FLASK_ENV", "development").lower()
    cfg = ProductionConfig if env == "production" else DevelopmentConfig
    app.config.from_object(cfg)

    # Configurações mínimas do flask-smorest / OpenAPI
    app.config.update({
        "API_TITLE": "MyClass API",
        "API_VERSION": "1.0",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_JSON_PATH": "/openapi.json",
        "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    })


def configure_logging(app: Flask):
    """Define logger padrão."""
    level = logging.DEBUG if (app.debug or app.testing) else logging.INFO
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    ))
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(level)


def register_error_handlers(app: Flask):
    """Handlers globais de erro (sem 404, para não interferir no Swagger)."""
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"erro": "Requisição inválida"}), 400

    @app.errorhandler(ValidationError)
    def handle_validation(err):
        return jsonify({"erros": err.messages}), 400

    @app.errorhandler(Exception)
    def internal_error(e):
        app.logger.exception(e)
        return jsonify({"erro": "Erro interno de servidor"}), 500


def register_extensions(app: Flask):
    """Inicializa extensões (ex: CORS)."""
    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))


def register_blueprints(api: Api):
    """Registra todos os blueprints do flask-smorest na Api."""
    api.register_blueprint(flashcard_bp)
    api.register_blueprint(curriculo_bp)
    api.register_blueprint(desafio_bp)
    api.register_blueprint(plano_bp)
    api.register_blueprint(quiz_bp)
    api.register_blueprint(user_bp)


def create_app() -> Flask:
    """Application factory."""
    app = Flask(__name__, instance_relative_config=False)

    # 1) Configurações gerais e OpenAPI
    configure_app(app)
    configure_logging(app)
    register_extensions(app)
    register_error_handlers(app)

    # 2) Monta o Api (Swagger + OpenAPI)
    api = Api(app)
    register_blueprints(api)

    # 3) Health check e redirect para Swagger UI
    @app.route("/")
    def index():
        return {"message": "API funcionando!", "docs": "/swagger-ui/"}

    @app.route("/swagger-ui")
    def swagger_ui_redirect():
        return redirect("/swagger-ui/", code=301)

    # 4) Rota de debug (apenas em desenvolvimento)
    if app.debug:
        @app.route("/debug")
        def debug():
            return {
                "blueprints": list(app.blueprints.keys()),
                "routes": [str(r) for r in app.url_map.iter_rules()],
                "openapi": {
                    k: v for k, v in app.config.items()
                    if k.startswith(("API_", "OPENAPI_"))
                }
            }

    return app
