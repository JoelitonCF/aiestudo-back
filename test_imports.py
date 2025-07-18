print("🔍 Testando imports...")

try:
    from flask_backend.services.user_service import criar_usuario, listar_usuarios
    print("✅ user_service importado com sucesso")

    # Teste básico
    user_id = criar_usuario("Teste", "teste@email.com")
    print(f"✅ Usuário criado: {user_id}")

    usuarios = listar_usuarios()
    print(f"✅ Usuários listados: {len(usuarios['items'])}")

except Exception as e:
    print(f"❌ Erro no user_service: {e}")

try:
    from flask_backend.services.desafio_service import gerar_desafio_diario
    print("✅ desafio_service importado com sucesso")

    # Teste básico
    desafio = gerar_desafio_diario("Matemática", "Porcentagem")
    print(f"✅ Desafio gerado: {desafio['questao'][:50]}...")

except Exception as e:
    print(f"❌ Erro no desafio_service: {e}")

try:
    from flask_backend.schemas.user_schema import UserSchema
    print("✅ user_schema importado com sucesso")
except Exception as e:
    print(f"❌ Erro no user_schema: {e}")

try:
    from flask_backend.schemas.desafio_schema import DesafioSchema
    print("✅ desafio_schema importado com sucesso")
except Exception as e:
    print(f"❌ Erro no desafio_schema: {e}")

print("\n🔍 Teste de imports concluído!")
