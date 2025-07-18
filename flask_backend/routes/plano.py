# flask_backend/routes/plano.py

from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_backend.schemas.plano_schema import PlanoSchema
from flask_backend.services import plano_service
from flask_backend.database import db

plano_bp = Blueprint('plano', __name__, url_prefix='/api/v1')


@plano_bp.arguments(PlanoSchema, location="json")
@plano_bp.response(201, description="Plano de estudos criado com sucesso")
@plano_bp.route("/planos", methods=["POST"])
def post_plano(plano_data):
    """Cria um novo plano de estudos personalizado."""
    try:
        plano_id = plano_service.gerar_plano(
            usuario_id=plano_data["usuario_id"],
            concurso=plano_data["concurso"],
            cargo=plano_data["cargo"],
            tempo_disponivel=plano_data.get(
                "tempo_disponivel", 2),  # horas por dia
            data_prova=plano_data.get("data_prova"),
            disciplinas_foco=plano_data.get("disciplinas_foco", [])
        )

        return {"plano_id": plano_id, "status": "criado"}, 201

    except Exception as e:
        abort(500, message=f"Erro ao criar plano: {str(e)}")


@plano_bp.response(200, description="Lista de planos de estudo")
@plano_bp.route("/planos", methods=["GET"])
def listar_planos():
    """Lista planos de estudo do usuário."""
    usuario_id = request.args.get("usuario_id")

    if not usuario_id:
        abort(400, message="usuario_id é obrigatório")

    try:
        planos = plano_service.listar_planos_usuario(usuario_id)
        return {"planos": planos}

    except Exception as e:
        abort(500, message=f"Erro ao listar planos: {str(e)}")


@plano_bp.response(200, description="Detalhes do plano de estudos")
@plano_bp.route("/planos/<plano_id>", methods=["GET"])
def obter_plano(plano_id):
    """Obtém detalhes de um plano específico."""
    try:
        plano = plano_service.obter_plano(plano_id)
        if not plano:
            abort(404, message="Plano não encontrado")

        return plano

    except Exception as e:
        abort(500, message=f"Erro ao obter plano: {str(e)}")


@plano_bp.arguments(PlanoSchema, location="json")
@plano_bp.response(200, description="Plano atualizado com sucesso")
@plano_bp.route("/planos/<plano_id>", methods=["PUT"])
def atualizar_plano(plano_data, plano_id):
    """Atualiza um plano de estudos."""
    try:
        plano_service.atualizar_plano(plano_id, plano_data)
        return {"message": "Plano atualizado com sucesso"}

    except Exception as e:
        abort(500, message=f"Erro ao atualizar plano: {str(e)}")


@plano_bp.response(200, description="Plano deletado com sucesso")
@plano_bp.route("/planos/<plano_id>", methods=["DELETE"])
def deletar_plano(plano_id):
    """Deleta um plano de estudos."""
    try:
        plano_service.deletar_plano(plano_id)
        return {"message": "Plano deletado com sucesso"}

    except Exception as e:
        abort(500, message=f"Erro ao deletar plano: {str(e)}")
