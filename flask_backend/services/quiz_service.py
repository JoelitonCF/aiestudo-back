# /services/quiz_service.py
from flask_backend.database import db
from datetime import datetime

COLL = "quizzes"


def start_quiz(user_id, questoes):
    data = {
        "usuario_id": user_id,
        "questoes": questoes,  # sem resposta do usuário ainda
        "acertos": 0,
        "erros": 0,
        "started_at": datetime.utcnow(),
        "finished_at": None,
        "tempo_total": None
    }
    _, ref = db.collection(COLL).add(data)
    return ref.id


def finish_quiz(quiz_id, respostas_do_usuario):
    ref = db.collection(COLL).document(quiz_id)
    doc = ref.get().to_dict()
    if doc["finished_at"]:
        raise ValueError("Quiz já finalizado")

    acertos = 0
    for i, q in enumerate(doc["questoes"]):
        correta = q.get("resposta_correta")
        given = respostas_do_usuario.get(str(i))
        doc["questoes"][i]["resposta_usuario"] = given
        if given == correta:
            acertos += 1

    erros = len(doc["questoes"]) - acertos
    finished = datetime.utcnow()
    tempo = (finished - doc["started_at"]).total_seconds()

    ref.update({
        "questoes": doc["questoes"],
        "acertos": acertos,
        "erros": erros,
        "finished_at": finished,
        "tempo_total": tempo
    })
    return {"acertos": acertos, "erros": erros, "tempo_total": tempo}
