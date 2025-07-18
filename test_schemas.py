print("🔍 Testando schemas...")

try:
    from flask_backend.schemas.desafio_schema import DesafioSchema

    schema = DesafioSchema()

    # Testar dados válidos
    test_data = {
        "disciplina": "Matemática",
        "subtopico": "Porcentagem",
        "nivel": "basico",
        "usuario": "João"
    }

    result = schema.load(test_data)
    print(f"✅ Schema válido: {result}")

except Exception as e:
    print(f"❌ Erro no schema: {e}")
    import traceback
    traceback.print_exc()

try:
    from flask_backend.schemas.user_schema import UserSchema

    schema = UserSchema()

    # Testar dados válidos
    test_data = {
        "nome": "João Silva",
        "email": "joao@test.com",
        "concurso_foco": "TJ-PA",
        "cargo_foco": "Analista"
    }

    result = schema.load(test_data)
    print(f"✅ User Schema válido: {result}")

except Exception as e:
    print(f"❌ Erro no user schema: {e}")
    import traceback
    traceback.print_exc()
