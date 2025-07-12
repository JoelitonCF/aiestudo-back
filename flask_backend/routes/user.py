from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.user_schema import UserCreateSchema, UserActivitySchema
from flask_backend.services import user_service
from flask_backend.database import db

user_bp = Blueprint('user', __name__, url_prefix='/api/v1')


@user_bp.route("/users/<user_id>", methods=["GET"])
def route_get_user(user_id):
    u = user_service.get_user(user_id)
    if not u:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    if u.get("last_activity"):
        u["last_activity"] = u["last_activity"].isoformat()
    return jsonify(u), 200


@user_bp.route("/users", methods=["POST"])
def route_create_user():
    payload = request.get_json() or {}
    payload = UserCreateSchema().load(payload)
    user_id = payload.get("user_id")
    nome = payload.get("nome")
    if not user_id or not nome:
        return jsonify({"erro": "user_id e nome são obrigatórios"}), 400
    u = user_service.create_user(user_id, nome)
    return jsonify(u), 201


@user_bp.route("/users/<user_id>/activity", methods=["POST"])
def route_add_activity(user_id):
    payload = request.get_json() or {}
    payload = UserActivitySchema().load(payload)
    xp = payload.get("xp")
    if xp is None:
        return jsonify({"erro": "xp é obrigatório"}), 400
    try:
        res = user_service.add_xp_and_update_streak(user_id, xp)
        return jsonify(res), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@user_bp.route("/users", methods=["GET"])
def list_users():
    users = []
    docs = db.collection("users").stream()
    for doc in docs:
        u = doc.to_dict()
        u["id"] = doc.id
        users.append(u)
    return jsonify({"ok": True, "usuarios": users})


@user_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json() or {}
    ref = db.collection("users").document(user_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Usuário não encontrado"}), 404
    ref.update(data)
    return jsonify({"ok": True, "mensagem": "Usuário atualizado"})


@user_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    ref = db.collection("users").document(user_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Usuário não encontrado"}), 404
    ref.delete()
    return jsonify({"ok": True, "mensagem": "Usuário removido"})
