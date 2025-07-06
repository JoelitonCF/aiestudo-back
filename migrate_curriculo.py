# migrate_curriculo.py
from flask_backend.database import db

COLL = "curriculos"  # ou Config.FIRESTORE_COLLECTION


def migrate():
    coll_ref = db.collection(COLL)
    for doc in coll_ref.stream():
        payload = doc.to_dict().get("dados")
        if payload:
            # sobrescreve o documento com os campos do payload no root
            coll_ref.document(doc.id).set(payload)
            print(f"Migrado {doc.id}")


if __name__ == "__main__":
    migrate()
