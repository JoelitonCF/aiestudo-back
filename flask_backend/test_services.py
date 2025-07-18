#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para validar os serviços refatorados.
"""

import sys
import traceback
import os
from datetime import datetime

# Configurar o path para importar os módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Simular estrutura de pacote se necessário
if 'flask_backend' not in sys.modules:
    import types
    flask_backend = types.ModuleType('flask_backend')
    sys.modules['flask_backend'] = flask_backend

def test_imports():
    """Testa se todos os imports estão funcionando."""
    print("🔍 Testando imports dos serviços...")
    
    try:
        # Testar imports dos serviços
        from services.flashcard_service import flashcard_service
        from services.user_service import user_service
        from services.curriculo_service import curriculo_service
        from services.base_service import BaseService
        
        # Testar imports dos utils
        from utils.validation_utils import validate_required_fields, sanitize_string
        from utils.response_utils import success_response, error_response
        
        print("✅ Todos os imports funcionaram!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no import: {e}")
        traceback.print_exc()
        return False

def test_base_service():
    """Testa funcionalidades da classe base."""
    print("\n🔍 Testando BaseService...")
    
    try:
        from services.base_service import BaseService
        
        # Criar uma instância de teste (mock)
        class TestService(BaseService):
            @property
            def collection_name(self):
                return "test_collection"
        
        service = TestService()
        
        # Testar se métodos existem
        assert hasattr(service, 'get_collection')
        assert hasattr(service, 'create')
        assert hasattr(service, 'get_by_id')
        assert hasattr(service, 'update')
        assert hasattr(service, 'delete')
        assert hasattr(service, 'find_by_field')
        
        print("✅ BaseService está funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no BaseService: {e}")
        traceback.print_exc()
        return False

def test_validation_utils():
    """Testa utilitários de validação."""
    print("\n🔍 Testando validation_utils...")
    
    try:
        from utils.validation_utils import validate_required_fields, sanitize_string
        
        # Testar validate_required_fields
        data = {"nome": "João", "idade": 25}
        required = ["nome", "idade", "email"]
        missing = validate_required_fields(data, required)
        assert missing == ["email"], f"Esperado ['email'], got {missing}"
        
        # Testar sanitize_string
        dirty_string = "  Olá Mundo!  "
        clean_string = sanitize_string(dirty_string)
        assert clean_string == "Olá Mundo!", f"Esperado 'Olá Mundo!', got '{clean_string}'"
        
        print("✅ validation_utils funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no validation_utils: {e}")
        traceback.print_exc()
        return False

def test_response_utils():
    """Testa utilitários de resposta."""
    print("\n🔍 Testando response_utils...")
    
    try:
        from utils.response_utils import success_response, error_response
        
        # Testar success_response
        response = success_response({"id": 123}, "Teste bem-sucedido")
        assert response["success"] == True
        assert response["data"]["id"] == 123
        assert "timestamp" in response
        
        # Testar error_response (versão atual do arquivo)
        error_resp, status_code = error_response("Erro de teste", 400)
        assert error_resp.json["success"] == False
        assert status_code == 400
        
        print("✅ response_utils funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no response_utils: {e}")
        traceback.print_exc()
        return False

def test_flashcard_service():
    """Testa o FlashcardService (métodos que não dependem do Firebase)."""
    print("\n🔍 Testando FlashcardService...")
    
    try:
        from services.flashcard_service import flashcard_service
        
        # Testar se a instância foi criada
        assert flashcard_service is not None
        assert hasattr(flashcard_service, 'criar_flashcard')
        assert hasattr(flashcard_service, 'listar_para_revisao')
        assert hasattr(flashcard_service, 'atualizar_revisao')
        assert hasattr(flashcard_service, 'get_estatisticas_usuario')
        
        # Testar métodos internos
        assert hasattr(flashcard_service, '_calculate_level')
        
        print("✅ FlashcardService estrutura OK!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no FlashcardService: {e}")
        traceback.print_exc()
        return False

def test_user_service():
    """Testa o UserService."""
    print("\n🔍 Testando UserService...")
    
    try:
        from services.user_service import user_service
        
        # Testar se a instância foi criada
        assert user_service is not None
        assert hasattr(user_service, 'create_user')
        assert hasattr(user_service, 'get_user')
        assert hasattr(user_service, 'add_xp_and_update_streak')
        assert hasattr(user_service, 'get_user_stats')
        
        # Testar métodos privados
        assert hasattr(user_service, '_calculate_level')
        assert hasattr(user_service, '_calculate_streak')
        
        # Testar cálculo de nível
        nivel1 = user_service._calculate_level(50)
        nivel2 = user_service._calculate_level(150)
        nivel3 = user_service._calculate_level(400)
        
        assert nivel1 == 1, f"Esperado nível 1, got {nivel1}"
        assert nivel2 == 2, f"Esperado nível 2, got {nivel2}"
        assert nivel3 == 3, f"Esperado nível 3, got {nivel3}"
        
        print("✅ UserService funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no UserService: {e}")
        traceback.print_exc()
        return False

def test_curriculo_service():
    """Testa o CurriculoService."""
    print("\n🔍 Testando CurriculoService...")
    
    try:
        from services.curriculo_service import curriculo_service
        
        # Testar se a instância foi criada
        assert curriculo_service is not None
        assert hasattr(curriculo_service, 'listar_curriculos')
        assert hasattr(curriculo_service, 'obter_curriculo')
        assert hasattr(curriculo_service, 'inserir_curriculo')
        assert hasattr(curriculo_service, 'buscar_por_disciplina')
        
        # Testar métodos privados
        assert hasattr(curriculo_service, '_generate_curriculo_id')
        assert hasattr(curriculo_service, '_count_total_topics')
        
        # Testar geração de ID
        test_id = curriculo_service._generate_curriculo_id("ENEM 2024", "Técnico/Assistente")
        expected_id = "enem_2024_técnico_assistente"
        assert test_id == expected_id, f"Esperado '{expected_id}', got '{test_id}'"
        
        # Testar contagem de tópicos
        disciplinas_test = [
            {"nome": "Matemática", "topicos": ["Álgebra", "Geometria"]},
            {"nome": "Português", "topicos": ["Gramática", "Literatura", "Redação"]}
        ]
        total_topicos = curriculo_service._count_total_topics(disciplinas_test)
        assert total_topicos == 5, f"Esperado 5 tópicos, got {total_topicos}"
        
        print("✅ CurriculoService funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no CurriculoService: {e}")
        traceback.print_exc()
        return False

def test_compatibility_functions():
    """Testa se as funções de compatibilidade ainda funcionam."""
    print("\n🔍 Testando funções de compatibilidade...")
    
    try:
        # Importar funções antigas
        from services.flashcard_service import criar_flashcard, listar_para_revisao
        from services.user_service import get_user, create_user
        from services.curriculo_service import listar_curriculos, obter_curriculo
        
        # Verificar se são callable
        assert callable(criar_flashcard)
        assert callable(listar_para_revisao)
        assert callable(get_user)
        assert callable(create_user)
        assert callable(listar_curriculos)
        assert callable(obter_curriculo)
        
        print("✅ Funções de compatibilidade OK!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas funções de compatibilidade: {e}")
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes."""
    print("🚀 Iniciando testes dos serviços refatorados...")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_base_service,
        test_validation_utils,
        test_response_utils,
        test_flashcard_service,
        test_user_service,
        test_curriculo_service,
        test_compatibility_functions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erro inesperado no teste {test.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Refatoração bem-sucedida!")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
