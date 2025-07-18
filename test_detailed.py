import requests
import json

BASE_URL = "http://localhost:5000"


def test_endpoint(method, url, data=None, description=""):
    """Testa um endpoint e exibe o resultado detalhado."""
    print(f"\n{'='*50}")
    print(f"🧪 {description}")
    print(f"{method} {url}")
    if data:
        print(f"Data: {json.dumps(data, indent=2, ensure_ascii=False)}")

    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers={
                                     'Content-Type': 'application/json'}, timeout=10)

        print(f"Status: {response.status_code}")

        try:
            result = response.json()
            print(
                f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        except:
            print(f"Response (text): {response.text}")

        return response.status_code == 200 or response.status_code == 201

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 Testando API MyClass")

    success_count = 0
    total_tests = 0

    # Teste 1: Health check
    total_tests += 1
    if test_endpoint("GET", f"{BASE_URL}/", description="Health Check"):
        success_count += 1

    # Teste 2: Listar tipos de desafio
    total_tests += 1
    if test_endpoint("GET", f"{BASE_URL}/api/v1/desafios/diario", description="Listar Tipos de Desafio"):
        success_count += 1

    # Teste 3: Criar usuário
    user_data = {
        "nome": "João Silva",
        "email": "joao@test.com",
        "concurso_foco": "TJ-PA",
        "cargo_foco": "Analista"
    }
    total_tests += 1
    if test_endpoint("POST", f"{BASE_URL}/api/v1/users", user_data, "Criar Usuário"):
        success_count += 1

    # Teste 4: Listar usuários
    total_tests += 1
    if test_endpoint("GET", f"{BASE_URL}/api/v1/users", description="Listar Usuários"):
        success_count += 1

    # Teste 5: Gerar desafio
    desafio_data = {
        "disciplina": "Matemática",
        "subtopico": "Porcentagem",
        "nivel": "basico",
        "usuario": "João"
    }
    total_tests += 1
    if test_endpoint("POST", f"{BASE_URL}/api/v1/desafios/diario", desafio_data, "Gerar Desafio"):
        success_count += 1

    # Resultado final
    print(f"\n{'='*50}")
    print(f"📊 Resultado Final: {success_count}/{total_tests} testes passaram")
    print(f"Taxa de sucesso: {(success_count/total_tests)*100:.1f}%")
