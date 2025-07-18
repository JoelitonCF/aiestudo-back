from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_backend.schemas.gerador_schema import GeradorSchema
from flask_backend.services import openai_service
from flask_backend.database import db

gerador_bp = Blueprint('gerador', __name__, url_prefix='/api/v1')


@gerador_bp.arguments(GeradorSchema, location="json")
@gerador_bp.response(200, description="Conteúdo gerado com sucesso")
@gerador_bp.route("/gerador/conteudo", methods=["POST"])
def gerar_conteudo(gerador_data):
    """Gera conteúdo educacional personalizado usando OpenAI."""
    try:
        tipo_conteudo = gerador_data["tipo"]
        disciplina = gerador_data["disciplina"]
        topico = gerador_data["topico"]
        nivel = gerador_data.get("nivel", "intermediario")
        formato = gerador_data.get("formato", "texto")

        if tipo_conteudo == "resumo":
            conteudo = openai_service.gerar_resumo(disciplina, topico, nivel)
        elif tipo_conteudo == "questoes":
            num_questoes = gerador_data.get("num_questoes", 5)
            conteudo = openai_service.gerar_questoes_quiz(
                disciplina, topico, num_questoes, nivel)
        elif tipo_conteudo == "plano_aula":
            conteudo = openai_service.gerar_plano_aula(
                disciplina, topico, nivel)
        elif tipo_conteudo == "exercicios":
            conteudo = openai_service.gerar_exercicios(
                disciplina, topico, nivel)
        else:
            abort(400, message="Tipo de conteúdo não suportado")

        return {
            "tipo": tipo_conteudo,
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "formato": formato,
            "conteudo": conteudo,
            "data_geracao": db.SERVER_TIMESTAMP
        }

    except Exception as e:
        abort(500, message=f"Erro ao gerar conteúdo: {str(e)}")


@gerador_bp.response(200, description="Lista de tipos de conteúdo disponíveis")
@gerador_bp.route("/gerador/tipos", methods=["GET"])
def listar_tipos_conteudo():
    """Lista tipos de conteúdo que podem ser gerados."""
    return {
        "tipos_conteudo": [
            {
                "id": "resumo",
                "nome": "Resumo",
                "descricao": "Resumo didático sobre o tópico"
            },
            {
                "id": "questoes",
                "nome": "Questões",
                "descricao": "Questões de múltipla escolha"
            },
            {
                "id": "plano_aula",
                "nome": "Plano de Aula",
                "descricao": "Plano de aula estruturado"
            },
            {
                "id": "exercicios",
                "nome": "Exercícios",
                "descricao": "Lista de exercícios práticos"
            }
        ],
        "niveis": ["basico", "intermediario", "avancado"],
        "formatos": ["texto", "markdown", "html"]
    }
