# /seed_curriculo.py
# flask_backend/seed_curriculo.py
import json
from pathlib import Path

# 1) importe do pacote flask_backend
from flask_backend.services.curriculo_service import inserir_curriculo

if __name__ == "__main__":
    # 2) localize o arquivo curriculo_seed.json
    base = Path(__file__).parent
    seed_file = base / "curriculo_seed.json"
    if not seed_file.exists():
        raise FileNotFoundError(f"Não achei {seed_file}")

    # 3) carregue e insira
    with open(seed_file, encoding="utf-8") as f:
        curr = json.load(f)

    doc_id = inserir_curriculo(curr)
    print("Inserido:", doc_id)
