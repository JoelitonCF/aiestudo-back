# flask_backend/routes/plano.py

from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.plano_schema import PlanoSchema
from flask_backend.services import plano_service

plano_bp = Blueprint('plano', __name__)


@plano_bp.route("/plano-estudo", methods=["POST"])
def criar_plano():
    payload = PlanoSchema().load(request.get_json() or {})
    plano = plano_service.gerar_plano(
        payload["concurso"], payload["cargo"], payload["dias"]
    )
    if plano is None:
        return jsonify({"erro": "Currículo não encontrado"}), 404
    return jsonify(plano), 201
