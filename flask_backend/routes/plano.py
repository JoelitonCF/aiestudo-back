# flask_backend/routes/plano.py

from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.plano_schema import PlanoSchema
from flask_backend.services import plano_service
from flask_backend.database import db

plano_bp = Blueprint('plano', __name__, url_prefix='/api/v1')


@plano_bp.route("/planos", methods=["POST"])
def criar_plano():
    payload = request.get_json() or {}
    payload = PlanoSchema().load(payload)
    concurso = payload.get("concurso", "")
    cargo = payload.get("cargo", "")
    dias = payload.get("dias", 30)
    if not concurso or not cargo:
        return jsonify({"erro": "Concurso e cargo são obrigatórios"}), 400
    plano = plano_service.gerar_plano(
        concurso, cargo, dias
    )
    if plano is None:
        return jsonify({"erro": "Currículo não encontrado"}), 404
    return jsonify(plano), 201

@plano_bp.route("/planos", methods=["GET"])
def list_planos():
    user_id = request.args.get("user_id")
    planos = []
    query = db.collection("planos")
    if user_id:
        query = query.where("usuario_id", "==", user_id)
    docs = query.stream()
    for doc in docs:
        p = doc.to_dict()
        p["id"] = doc.id
        planos.append(p)
    return jsonify({"ok": True, "planos": planos})

@plano_bp.route("/planos/<plano_id>", methods=["GET"])
def get_plano(plano_id):
    doc = db.collection("planos").document(plano_id).get()
    if not doc.exists:
        return jsonify({"ok": False, "erro": "Plano não encontrado"}), 404
    plano = doc.to_dict()
    plano["id"] = doc.id
    return jsonify({"ok": True, "plano": plano})

@plano_bp.route("/planos/<plano_id>", methods=["PUT"])
def update_plano(plano_id):
    data = request.get_json() or {}
    ref = db.collection("planos").document(plano_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Plano não encontrado"}), 404
    ref.update(data)
    return jsonify({"ok": True, "mensagem": "Plano atualizado"})

@plano_bp.route("/planos/<plano_id>", methods=["DELETE"])
def delete_plano(plano_id):
    ref = db.collection("planos").document(plano_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Plano não encontrado"}), 404
    ref.delete()
    return jsonify({"ok": True, "mensagem": "Plano removido"})
