import os
import logging
from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flask_smorest import Api
from marshmallow import ValidationError


def create_app():
    app = Flask(__name__)

    # Configuração básica
    app.config['API_TITLE'] = 'MyClass API'
    app.config['API_VERSION'] = '1.0'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_JSON_PATH'] = '/openapi.json'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['OPENAPI_URL_PREFIX'] = ''

    # CORS
    CORS(app)

    # Flask-Smorest API
    api = Api(app)

    # Registrar blueprint simples (sem Flask-Smorest)
    try:
        from .routes.test_simple import simple_bp
        app.register_blueprint(simple_bp)
        print("✅ Blueprint simples registrado")
    except Exception as e:
        print(f"❌ Erro no blueprint simples: {e}")

    # Importar e registrar blueprints com Flask-Smorest
    try:
        from .routes.flashcard import flashcard_bp
        from .routes.curriculo import curriculo_bp
        from .routes.desafio import desafio_bp
        from .routes.plano import plano_bp
        from .routes.quiz import quiz_bp
        from .routes.user import user_bp
        from .routes.gerador import gerador_bp

        api.register_blueprint(flashcard_bp)
        api.register_blueprint(curriculo_bp)
        api.register_blueprint(desafio_bp)
        api.register_blueprint(plano_bp)
        api.register_blueprint(quiz_bp)
        api.register_blueprint(user_bp)
        api.register_blueprint(gerador_bp)

        print("✅ Todos os blueprints Flask-Smorest registrados")

    except Exception as e:
        print(f"❌ Erro ao registrar blueprints Flask-Smorest: {e}")
        import traceback
        traceback.print_exc()

    # Rotas básicas
    @app.route('/')
    def index():
        return jsonify({'message': 'API MyClass está funcionando!'})

    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'erro': 'Requisição inválida'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'erro': 'Recurso não encontrado'}), 404

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({'erro': 'Dados inválidos', 'detalhes': error.messages}), 400

    @app.errorhandler(Exception)
    def handle_general_error(error):
        app.logger.error(f'Erro não tratado: {str(error)}')
        return jsonify({'erro': 'Erro interno de servidor'}), 500

    return app
