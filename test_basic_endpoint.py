import requests
import json

BASE_URL = "http://localhost:5000"


def test_simple_post():
    """Teste POST mais simples possível"""

    # Teste 1: POST direto para desafio (sem usar o schema)
    print("🧪 Testando POST direto...")

    try:
        # Fazer request POST bem simples
        response = requests.post(
            f"{BASE_URL}/api/v1/desafios/diario",
            headers={'Content-Type': 'application/json'},
            data='{"disciplina": "Matemática", "subtopico": "Soma", "nivel": "basico"}'
        )

        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    test_simple_post()
