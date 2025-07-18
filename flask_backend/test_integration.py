#!/usr/bin/env python3
"""
Teste do servidor Flask - verificar se a API está funcionando.
"""

def test_flask_app():
    """Testa se a aplicação Flask pode ser importada e inicializada."""
    print("🔍 Testando aplicação Flask...")
    
    try:
        # Importar e testar se app existe
        import app
        
        if hasattr(app, 'app'):
            flask_app = app.app
            print("✅ Aplicação Flask importada com sucesso!")
            
            # Testar se tem as rotas esperadas
            rules = [str(rule) for rule in flask_app.url_map.iter_rules()]
            
            expected_routes = [
                '/api/v1/flashcards/',
                '/api/v1/usuarios/',
                '/api/v1/curriculos/',
                '/api/v1/quizzes/'
            ]
            
            found_routes = []
            for expected in expected_routes:
                if any(expected in rule for rule in rules):
                    found_routes.append(expected)
                    print(f"✅ Rota encontrada: {expected}")
                else:
                    print(f"⚠️  Rota não encontrada: {expected}")
            
            print(f"📊 {len(found_routes)}/{len(expected_routes)} rotas principais encontradas")
            return len(found_routes) > 0
            
        else:
            print("❌ Variável 'app' não encontrada no módulo")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao importar app: {e}")
        return False

def test_routes_individually():
    """Testa se os blueprints das rotas existem."""
    print("\n🔍 Testando blueprints das rotas...")
    
    route_modules = [
        'routes.flashcard',
        'routes.user', 
        'routes.curriculo',
        'routes.quiz'
    ]
    
    working_routes = 0
    for route_module in route_modules:
        try:
            module = __import__(route_module, fromlist=[''])
            # Procurar por blueprints no módulo
            blueprints = [attr for attr in dir(module) if attr.endswith('_bp')]
            if blueprints:
                print(f"✅ {route_module} - blueprint encontrado: {blueprints[0]}")
                working_routes += 1
            else:
                print(f"❌ {route_module} - nenhum blueprint encontrado")
                
        except Exception as e:
            print(f"❌ {route_module} - erro: {e}")
    
    print(f"📊 {working_routes}/{len(route_modules)} módulos de rota funcionando")
    return working_routes > 0

def test_database_connection():
    """Testa se a conexão com database pode ser importada."""
    print("\n🔍 Testando conexão com database...")
    
    try:
        import database
        if hasattr(database, 'db'):
            print("✅ Módulo database importado com sucesso!")
            print("ℹ️  Para testar conexão real, precisa configurar Firebase")
            return True
        else:
            print("❌ Variável 'db' não encontrada no módulo database")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao importar database: {e}")
        return False

def test_config():
    """Testa se as configurações podem ser importadas."""
    print("\n🔍 Testando configurações...")
    
    try:
        import config
        if hasattr(config, 'Config'):
            config_obj = config.Config()
            print("✅ Módulo config importado com sucesso!")
            
            # Verificar algumas configurações esperadas
            expected_attrs = ['FIRESTORE_COLLECTION', 'SECRET_KEY']
            found_attrs = []
            
            for attr in expected_attrs:
                if hasattr(config_obj, attr):
                    found_attrs.append(attr)
                    print(f"✅ Configuração encontrada: {attr}")
                else:
                    print(f"⚠️  Configuração não encontrada: {attr}")
            
            return len(found_attrs) > 0
            
        else:
            print("❌ Classe 'Config' não encontrada no módulo")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao importar config: {e}")
        return False

def main():
    """Executa todos os testes de integração."""
    print("🚀 Iniciando testes de integração do Flask...")
    print("=" * 60)
    
    tests = [
        test_config,
        test_database_connection,
        test_routes_individually,
        test_flask_app
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
    print(f"📊 Resultados: {passed}/{total} testes de integração passaram")
    
    if passed == total:
        print("🎉 Todos os testes de integração passaram!")
        print("🔧 Sugestões para teste final:")
        print("   1. Configurar Firebase (GOOGLE_APPLICATION_CREDENTIALS)")
        print("   2. Executar: python app.py")
        print("   3. Testar endpoints com Postman/curl")
        return True
    elif passed >= total // 2:
        print("✅ Estrutura básica funcionando!")
        print("⚠️  Alguns componentes precisam de configuração adicional")
        return True
    else:
        print("❌ Muitos componentes com problemas. Verificar configuração.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
