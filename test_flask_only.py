print("🔍 Testando Flask com imports...")

try:
    # Testar imports do Flask
    from flask import Flask
    from flask_smorest import Api, Blueprint
    from marshmallow import Schema, fields
    print("✅ Flask e dependências OK")

    # Testar criação básica da app
    app = Flask(__name__)
    app.config['API_TITLE'] = 'Test API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'

    api = Api(app)
    print("✅ Flask-Smorest configurado")

    # Testar schema básico
    class TestSchema(Schema):
        nome = fields.String()

    # Testar blueprint básico
    test_bp = Blueprint('test', __name__)

    @test_bp.route('/test')
    def test_route():
        return {"message": "OK"}

    api.register_blueprint(test_bp)
    print("✅ Blueprint registrado")

    # Testar import dos nossos serviços
    from flask_backend.services.user_service import criar_usuario
    from flask_backend.services.desafio_service import gerar_desafio_diario
    print("✅ Nossos serviços importados no contexto Flask")

    print("✅ Todos os testes passaram!")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
