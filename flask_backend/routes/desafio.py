from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.desafio_schema import DesafioSchema
from flask_backend.services import openai_service

desafio_bp = Blueprint('desafio', __name__)


@desafio_bp.route("/desafio-diario", methods=["POST"])
def desafio_diario():
    body = DesafioSchema().load(request.get_json() or {})
    resultado = openai_service.gerar_desafio_ia(
        body["usuario"], body["disciplina"], body["subtopico"], body["nivel"]
    )
    return jsonify(resultado), 200
