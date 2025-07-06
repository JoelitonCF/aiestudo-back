# flask_backend/services/flashcard_service.py
from flask_backend.database import db
from datetime import datetime, timedelta

COLL = "flashcards"


def criar_flashcard(usuario_id, disciplina, topico, subtopico, pergunta, resposta):
    data = {
        "usuario_id":   usuario_id,
        "disciplina":   disciplina,
        "topico":       topico,
        "subtopico":    subtopico,
        "pergunta":     pergunta,
        "resposta":     resposta,
        "intervalo":    1,  # dias iniciais
        "proxima_revisao": datetime.utcnow(),
        "acertos":      0,
        "erros":        0
    }
    _, ref = db.collection(COLL).add(data)
    return ref.id


def listar_para_revisao(usuario_id: str, limit: int = 20, start_after_id: str = None):
    agora = datetime.utcnow()
    query = (db.collection(COLL)
               .where("usuario_id", "==", usuario_id)
               .where("proxima_revisao", "<=", agora)
               .order_by("proxima_revisao"))
    if start_after_id:
        last = db.collection(COLL).document(start_after_id).get()
        if last.exists:
            query = query.start_after(last)
    docs = query.limit(limit).stream()
    items, last_id = [], None
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        items.append(d)
        last_id = doc.id
    return {"items": items, "nextPageToken": last_id}


def atualizar_revisao(card_id, acerto: bool):
    ref = db.collection(COLL).document(card_id)
    doc = ref.get().to_dict()
    intervalo = doc["intervalo"]
    if acerto:
        novo_intervalo = intervalo * 2
        acertos = doc["acertos"] + 1
        erros = doc["erros"]
    else:
        novo_intervalo = 1
        acertos = doc["acertos"]
        erros = doc["erros"] + 1

    proxima = datetime.utcnow() + timedelta(days=novo_intervalo)
    ref.update({
        "intervalo": novo_intervalo,
        "proxima_revisao": proxima,
        "acertos": acertos,
        "erros": erros
    })
    return True
