from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.desafio_schema import DesafioSchema
from flask_backend.services import openai_service
from flask_backend.database import db

desafio_bp = Blueprint('desafio', __name__, url_prefix='/api/v1')


@desafio_bp.route("/desafios/diario", methods=["POST"])
def desafio_diario():
    body = request.get_json() or {}
    body = DesafioSchema().load(body)
    usuario = body.get("usuario", "Aluno")
    disciplina = body.get("disciplina", "")
    subtopico = body.get("subtopico", "")
    nivel = body.get("nivel", "TJ-PA")
    if not disciplina or not subtopico:
        return jsonify({"erro": "Disciplina e subtopico são obrigatórios"}), 400
    resultado = openai_service.gerar_desafio_ia(
        usuario, disciplina, subtopico, nivel
    )
    return jsonify(resultado), 200

@desafio_bp.route("/desafios/diario", methods=["GET"])
def list_desafios_diario():
    user_id = request.args.get("user_id")
    desafios = []
    query = db.collection("desafios_diarios")
    if user_id:
        query = query.where("usuario_id", "==", user_id)
    docs = query.stream()
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        desafios.append(d)
    return jsonify({"ok": True, "desafios": desafios})
