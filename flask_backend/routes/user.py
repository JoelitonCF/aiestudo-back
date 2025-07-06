from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.user_schema import UserCreateSchema, UserActivitySchema
from flask_backend.services import user_service

user_bp = Blueprint('user', __name__)


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
    payload = UserCreateSchema().load(request.get_json() or {})
    u = user_service.create_user(payload["user_id"], payload["nome"])
    return jsonify(u), 201


@user_bp.route("/users/<user_id>/activity", methods=["POST"])
def route_add_activity(user_id):
    payload = UserActivitySchema().load(request.get_json() or {})
    try:
        res = user_service.add_xp_and_update_streak(user_id, payload["xp"])
        return jsonify(res), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404
