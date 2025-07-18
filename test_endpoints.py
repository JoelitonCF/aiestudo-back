import requests
import json

BASE_URL = "http://localhost:5000"


def test_endpoint(method, url, data=None):
    """Testa um endpoint e exibe o resultado."""
    print(f"\n🧪 {method} {url}")

    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={
                                     'Content-Type': 'application/json'})
        elif method == "PUT":
            response = requests.put(url, json=data, headers={
                                    'Content-Type': 'application/json'})
        elif method == "DELETE":
            response = requests.delete(url)

        print(f"Status: {response.status_code}")

        try:
            result = response.json()
            print(
                f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        except:
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"Erro: {str(e)}")


if __name__ == "__main__":
    # Testar endpoints básicos
    test_endpoint("GET", f"{BASE_URL}/")
    test_endpoint("GET", f"{BASE_URL}/api/v1/desafios/diario")

    # Testar criação de usuário
    user_data = {
        "nome": "João Silva",
        "email": "joao@test.com",
        "concurso_foco": "TJ-PA",
        "cargo_foco": "Analista"
    }
    test_endpoint("POST", f"{BASE_URL}/api/v1/users", user_data)

    # Testar geração de desafio
    desafio_data = {
        "disciplina": "Matemática",
        "subtopico": "Porcentagem",
        "nivel": "basico"
    }
    test_endpoint("POST", f"{BASE_URL}/api/v1/desafios/diario", desafio_data)
