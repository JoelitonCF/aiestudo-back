import requests
import json

BASE_URL = "http://localhost:5000"


def test_simple_endpoints():
    print("🧪 Testando endpoints SIMPLES...")

    # Teste 1: Criar usuário (endpoint simples)
    print("\n1. Testando criação de usuário (simples):")
    response = requests.post(
        f"{BASE_URL}/api/v1/simple/users",
        json={
            "nome": "João Silva",
            "email": "joao@test.com",
            "concurso_foco": "TJ-PA",
            "cargo_foco": "Analista"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Teste 2: Listar usuários (endpoint simples)
    print("\n2. Testando listagem de usuários (simples):")
    response = requests.get(f"{BASE_URL}/api/v1/simple/users")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Teste 3: Gerar desafio (endpoint simples)
    print("\n3. Testando geração de desafio (simples):")
    response = requests.post(
        f"{BASE_URL}/api/v1/simple/desafios",
        json={
            "disciplina": "Matemática",
            "subtopico": "Porcentagem",
            "nivel": "basico",
            "usuario": "João"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    test_simple_endpoints()
