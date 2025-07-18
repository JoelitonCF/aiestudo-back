# flask_backend/routes/quiz.py

from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_backend.schemas.quiz_schema import QuizStartSchema, QuizFinishSchema
from flask_backend.services import quiz_service
from flask_backend.database import db

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/v1')


@quiz_bp.arguments(QuizStartSchema, location="json")
@quiz_bp.response(201, description="Quiz iniciado com sucesso")
@quiz_bp.route("/quizzes", methods=["POST"])
def post_quiz(quiz_data):
    """Inicia um novo quiz."""
    try:
        resultado = quiz_service.start_quiz(
            usuario_id=quiz_data["usuario_id"],
            disciplina=quiz_data["disciplina"],
            subtopico=quiz_data.get("subtopico"),
            num_questoes=quiz_data.get("num_questoes", 10),
            nivel=quiz_data.get("nivel", "intermediario")
        )

        return resultado, 201

    except Exception as e:
        abort(500, message=f"Erro ao iniciar quiz: {str(e)}")


@quiz_bp.arguments(QuizFinishSchema, location="json")
@quiz_bp.response(200, description="Quiz finalizado com sucesso")
@quiz_bp.route("/quizzes/<quiz_id>/finish", methods=["POST"])
def finish_quiz(quiz_finish_data, quiz_id):
    """Finaliza um quiz e calcula o resultado."""
    try:
        resultado = quiz_service.finish_quiz(
            quiz_id=quiz_id,
            respostas=quiz_finish_data["respostas"]
        )

        return {
            "quiz_id": quiz_id,
            "resultado": resultado,
            "status": "finalizado"
        }

    except Exception as e:
        abort(500, message=f"Erro ao finalizar quiz: {str(e)}")


@quiz_bp.response(200, description="Lista de quizzes do usuário")
@quiz_bp.route("/quizzes", methods=["GET"])
def listar_quizzes():
    """Lista quizzes disponíveis ou do usuário."""
    usuario_id = request.args.get("usuario_id")

    try:
        if usuario_id:
            quizzes = quiz_service.listar_quizzes_usuario(usuario_id)
        else:
            quizzes = quiz_service.listar_quizzes_publicos()

        return {"quizzes": quizzes}

    except Exception as e:
        abort(500, message=f"Erro ao listar quizzes: {str(e)}")


@quiz_bp.response(200, description="Detalhes do quiz")
@quiz_bp.route("/quizzes/<quiz_id>", methods=["GET"])
def obter_quiz(quiz_id):
    """Obtém detalhes de um quiz específico."""
    try:
        quiz = quiz_service.obter_quiz(quiz_id)
        if not quiz:
            abort(404, message="Quiz não encontrado")

        return quiz

    except Exception as e:
        abort(500, message=f"Erro ao obter quiz: {str(e)}")


@quiz_bp.response(200, description="Quiz deletado com sucesso")
@quiz_bp.route("/quizzes/<quiz_id>", methods=["DELETE"])
def deletar_quiz(quiz_id):
    """Deleta um quiz."""
    try:
        quiz_service.deletar_quiz(quiz_id)
        return {"message": "Quiz deletado com sucesso"}

    except Exception as e:
        abort(500, message=f"Erro ao deletar quiz: {str(e)}")
