# flask_backend/routes/quiz.py

from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.quiz_schema import QuizStartSchema, QuizFinishSchema
from flask_backend.services import quiz_service
from flask_backend.database import db

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/v1')


@quiz_bp.route("/quizzes", methods=["POST"])
def post_quiz():
    payload = request.get_json() or {}
    payload = QuizStartSchema().load(payload)
    usuario_id = payload.get("usuario_id")
    questoes = payload.get("questoes")
    if not usuario_id or not questoes:
        return jsonify({"erro": "usuario_id e questoes são obrigatórios"}), 400
    quiz_id = quiz_service.start_quiz(
        usuario_id, questoes)
    return jsonify({"quiz_id": quiz_id}), 201


@quiz_bp.route("/quizzes/<quiz_id>/finish", methods=["POST"])
def finish_quiz_route(quiz_id):
    payload = request.get_json() or {}
    payload = QuizFinishSchema().load(payload)
    respostas = payload.get("respostas")
    if not respostas:
        return jsonify({"erro": "respostas são obrigatórias"}), 400
    try:
        res = quiz_service.finish_quiz(quiz_id, respostas)
        return jsonify(res), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400


@quiz_bp.route("/quizzes", methods=["GET"])
def list_quizzes():
    user_id = request.args.get("user_id")
    quizzes = []
    query = db.collection("quizzes")
    if user_id:
        query = query.where("usuario_id", "==", user_id)
    docs = query.stream()
    for doc in docs:
        q = doc.to_dict()
        q["id"] = doc.id
        quizzes.append(q)
    return jsonify({"ok": True, "quizzes": quizzes})


@quiz_bp.route("/quizzes/<quiz_id>", methods=["GET"])
def get_quiz(quiz_id):
    doc = db.collection("quizzes").document(quiz_id).get()
    if not doc.exists:
        return jsonify({"ok": False, "erro": "Quiz não encontrado"}), 404
    quiz = doc.to_dict()
    quiz["id"] = doc.id
    return jsonify({"ok": True, "quiz": quiz})


@quiz_bp.route("/quizzes/<quiz_id>", methods=["DELETE"])
def delete_quiz(quiz_id):
    ref = db.collection("quizzes").document(quiz_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Quiz não encontrado"}), 404
    ref.delete()
    return jsonify({"ok": True, "mensagem": "Quiz removido"})
