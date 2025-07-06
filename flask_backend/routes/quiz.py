# flask_backend/routes/quiz.py

from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.quiz_schema import QuizStartSchema, QuizFinishSchema
from flask_backend.services import quiz_service

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route("/quiz", methods=["POST"])
def post_quiz():
    # valida e desserializa com Marshmallow
    payload = QuizStartSchema().load(request.get_json() or {})
    # chama o serviço via módulo, que será monkeypatchável
    quiz_id = quiz_service.start_quiz(
        payload["usuario_id"], payload["questoes"])
    return jsonify({"quiz_id": quiz_id}), 201


@quiz_bp.route("/quiz/<quiz_id>/finish", methods=["POST"])
def finish_quiz_route(quiz_id):
    payload = QuizFinishSchema().load(request.get_json() or {})
    try:
        res = quiz_service.finish_quiz(quiz_id, payload["respostas"])
        return jsonify(res), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
