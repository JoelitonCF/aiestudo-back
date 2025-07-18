from flask_backend import create_app
import traceback


if __name__ == "__main__":
    try:
        app = create_app()
        print("🚀 Aplicação Flask criada com sucesso!")
        print("📋 Rotas registradas:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.methods} {rule.rule}")

        app.run(debug=True, host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"❌ Erro ao criar aplicação: {e}")
        traceback.print_exc()
