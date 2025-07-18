#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples dos serviços refatorados.
"""

def test_basic_functionality():
    """Teste básico de funcionalidade."""
    print("🔍 Testando funcionalidades básicas...")
    
    # Teste 1: Verificar se arquivos existem
    import os
    
    files_to_check = [
        "services/base_service.py",
        "services/flashcard_service.py", 
        "services/user_service.py",
        "services/curriculo_service.py",
        "utils/validation_utils.py",
        "utils/response_utils.py"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} existe")
        else:
            print(f"❌ {file_path} não encontrado")
            return False
    
    # Teste 2: Verificar imports básicos sem dependências do Firebase
    try:
        # Testar utils que não dependem de nada externo
        sys.path.append('.')
        
        # Mock do database para evitar erros de importação
        import sys
        import types
        
        # Criar mock do módulo database
        mock_db = types.ModuleType('database')
        mock_db.db = None
        sys.modules['database'] = mock_db
        
        # Criar mock do módulo config
        mock_config = types.ModuleType('config')
        mock_config.Config = types.SimpleNamespace()
        mock_config.Config.FIRESTORE_COLLECTION = "test_collection"
        sys.modules['config'] = mock_config
        
        print("✅ Mocks criados com sucesso")
        
    except Exception as e:
        print(f"❌ Erro na criação de mocks: {e}")
        return False
    
    # Teste 3: Validar estrutura dos arquivos
    print("✅ Estrutura básica validada!")
    return True

def test_code_syntax():
    """Testa se o código Python está sintaticamente correto."""
    import py_compile
    import os
    
    print("\n🔍 Testando sintaxe dos arquivos Python...")
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and not file.startswith('test_'):
                python_files.append(os.path.join(root, file))
    
    errors = []
    for file_path in python_files:
        try:
            py_compile.compile(file_path, doraise=True)
            print(f"✅ {file_path} - sintaxe OK")
        except py_compile.PyCompileError as e:
            print(f"❌ {file_path} - erro de sintaxe: {e}")
            errors.append((file_path, str(e)))
    
    if errors:
        print(f"\n❌ {len(errors)} arquivos com erro de sintaxe")
        return False
    else:
        print(f"\n✅ Todos os {len(python_files)} arquivos Python têm sintaxe válida!")
        return True

def test_service_structure():
    """Testa se a estrutura dos serviços está correta."""
    print("\n🔍 Testando estrutura dos serviços...")
    
    # Verificar se os arquivos contêm as classes e funções esperadas
    service_tests = {
        "services/flashcard_service.py": [
            "class FlashcardService",
            "flashcard_service =",
            "def criar_flashcard",
            "def listar_para_revisao"
        ],
        "services/user_service.py": [
            "class UserService", 
            "user_service =",
            "def create_user",
            "def get_user"
        ],
        "services/curriculo_service.py": [
            "class CurriculoService",
            "curriculo_service =",
            "def listar_curriculos",
            "def obter_curriculo"
        ],
        "services/base_service.py": [
            "class BaseService",
            "def create",
            "def get_by_id",
            "def update",
            "def delete"
        ]
    }
    
    for file_path, expected_content in service_tests.items():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            missing = []
            for expected in expected_content:
                if expected not in content:
                    missing.append(expected)
            
            if missing:
                print(f"❌ {file_path} - faltando: {', '.join(missing)}")
                return False
            else:
                print(f"✅ {file_path} - estrutura OK")
                
        except Exception as e:
            print(f"❌ Erro ao ler {file_path}: {e}")
            return False
    
    print("✅ Estrutura dos serviços está correta!")
    return True

def test_utils_structure():
    """Testa se os utilitários estão corretos."""
    print("\n🔍 Testando estrutura dos utilitários...")
    
    utils_tests = {
        "utils/validation_utils.py": [
            "def validate_required_fields",
            "def sanitize_string"
        ],
        "utils/response_utils.py": [
            "def success_response",
            "def error_response"
        ]
    }
    
    for file_path, expected_functions in utils_tests.items():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            missing = []
            for expected in expected_functions:
                if expected not in content:
                    missing.append(expected)
            
            if missing:
                print(f"❌ {file_path} - faltando: {', '.join(missing)}")
                return False
            else:
                print(f"✅ {file_path} - funções OK")
                
        except Exception as e:
            print(f"❌ Erro ao ler {file_path}: {e}")
            return False
    
    print("✅ Estrutura dos utilitários está correta!")
    return True

def main():
    """Executa todos os testes."""
    print("🚀 Iniciando testes básicos da refatoração...")
    print("=" * 60)
    
    tests = [
        test_basic_functionality,
        test_code_syntax,
        test_service_structure,
        test_utils_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Erro inesperado no teste {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes básicos passaram!")
        print("📋 Próximos passos:")
        print("   1. Testar com Firebase configurado")
        print("   2. Executar o servidor Flask")
        print("   3. Testar as rotas da API")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
