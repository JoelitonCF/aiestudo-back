# /services/user_service.py
from flask_backend.database import db
from datetime import datetime, timedelta

COLL = "users"


def get_user(user_id):
    doc = db.collection(COLL).document(user_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


def create_user(user_id, nome):
    data = {
        "nome": nome,
        "xp": 0,
        "streak": 0,
        "last_activity": None,
        "created_at": datetime.utcnow()
    }
    db.collection(COLL).document(user_id).set(data)
    return data


def add_xp_and_update_streak(user_id, xp_earned):
    ref = db.collection(COLL).document(user_id)
    doc = ref.get().to_dict()
    if not doc:
        raise ValueError("Usuário não encontrado")

    now = datetime.utcnow()
    last = doc.get("last_activity")
    streak = doc.get("streak", 0)
    # Se a última atividade foi ontem, incrementa streak; se hoje mantém; senão zera
    if last:
        delta = now.date() - last.date()
        if delta == timedelta(days=1):
            streak += 1
        elif delta > timedelta(days=1):
            streak = 1
    else:
        streak = 1

    xp = doc.get("xp", 0) + xp_earned

    ref.update({
        "xp": xp,
        "streak": streak,
        "last_activity": now
    })
    return {"xp": xp, "streak": streak}
