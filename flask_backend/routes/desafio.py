from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_backend.schemas.desafio_schema import DesafioSchema
from flask_backend.services.desafio_service import gerar_desafio_diario

desafio_bp = Blueprint('desafio', __name__, url_prefix='/api/v1')


@desafio_bp.arguments(DesafioSchema, location="json")
@desafio_bp.response(200, description="Desafio gerado com sucesso")
@desafio_bp.route("/desafios/diario", methods=["POST"])
def desafio_diario(desafio_data):
    """Gera um desafio diário personalizado."""
    try:
        usuario = desafio_data.get("usuario", "Aluno")
        disciplina = desafio_data["disciplina"]
        subtopico = desafio_data["subtopico"]
        nivel = desafio_data.get("nivel", "intermediario")

        # Usar serviço simplificado
        desafio = gerar_desafio_diario(
            disciplina=disciplina,
            subtopico=subtopico,
            nivel=nivel,
            usuario=usuario
        )

        return {
            "sucesso": True,
            "desafio": desafio,
            "usuario": usuario
        }

    except Exception as e:
        abort(500, message=f"Erro ao gerar desafio: {str(e)}")


@desafio_bp.response(200, description="Lista de desafios disponíveis")
@desafio_bp.route("/desafios/diario", methods=["GET"])
def listar_desafios():
    """Lista tipos de desafios disponíveis."""
    return {
        "tipos": [
            "questao_multipla_escolha",
            "questao_dissertativa",
            "caso_pratico",
            "exercicio_aplicacao"
        ],
        "niveis": ["basico", "intermediario", "avancado"],
        "disciplinas_disponiveis": [
            "Língua Portuguesa",
            "Direito Constitucional",
            "Direito Administrativo",
            "Matemática",
            "Informática"
        ]
    }
