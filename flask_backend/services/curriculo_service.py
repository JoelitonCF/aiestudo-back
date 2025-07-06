
# flask_backend/services/curriculo_service.py
from flask_backend.database import db
from flask_backend.config import Config
from typing import Optional, Dict

COLL = Config.FIRESTORE_COLLECTION  # ex: "curriculos"


def listar_curriculos(limit: int = 20, start_after_id: str = None) -> Dict:
    col = db.collection(COLL).order_by("concurso")
    if start_after_id:
        last = db.collection(COLL).document(start_after_id).get()
        if last.exists:
            col = col.start_after(last)
    docs = col.limit(limit).stream()
    items = []
    last_id = None
    for doc in docs:
        data = doc.to_dict()
        items.append({
            "id": doc.id,
            "concurso": data.get("concurso"),
            "cargo": data.get("cargo")
        })
        last_id = doc.id
    return {"items": items, "nextPageToken": last_id}


def obter_curriculo(concurso: str, cargo: str) -> Optional[Dict]:
    doc_id = f"{concurso}_{cargo}".replace(" ", "")
    doc = db.collection(COLL).document(doc_id).get()
    if not doc.exists:
        return None
    return doc.to_dict()


def inserir_curriculo(curriculo: Dict) -> str:
    doc_id = f"{curriculo['concurso']}_{curriculo['cargo']}".replace(" ", "")
    # agora gravamos o payload diretamente, sem subcampo "dados"
    db.collection(COLL).document(doc_id).set(curriculo)
    return doc_id
