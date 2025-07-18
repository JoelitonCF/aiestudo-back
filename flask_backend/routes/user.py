from flask import request, jsonify
from flask import request
from flask_smorest import Blueprint, abort
from flask_backend.schemas.user_schema import UserSchema, UserActivitySchema
from flask_backend.services.user_service import (
    criar_usuario,
    listar_usuarios,
    obter_usuario,
    atualizar_usuario,
    deletar_usuario,
    registrar_atividade
)

user_bp = Blueprint('user', __name__, url_prefix='/api/v1/users')


# @user_bp.arguments(UserSchema, location="json")  # ← Comente esta linha
@user_bp.response(201, description="Usuário criado com sucesso")
@user_bp.route("/", methods=["POST"])
def criar_usuario_endpoint():  # ← Remova o parâmetro user_data
    """Cria um novo usuário."""
    try:
        # Pegar dadoss diretamente do request 
        user_data = request.get_json()

        # Validação manual básica
        if not user_data or not user_data.get("nome") or not user_data.get("email"):
            return {"erro": "Nome e email são obrigatórios"}, 400

        user_id = criar_usuario(
            nome=user_data["nome"],
            email=user_data["email"],
            concurso_foco=user_data.get("concurso_foco"),
            cargo_foco=user_data.get("cargo_foco")
        )

        print(f"🔍 DEBUG: User ID criado: {user_id}")
        return {"user_id": user_id, "status": "criado"}, 201

    except Exception as e:
        print(f"❌ ERRO ESPECÍFICO: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"erro": str(e)}, 500


@user_bp.response(200, description="Lista de usuários")
@user_bp.route("/", methods=["GET"])
def listar_usuarios_endpoint():
    """Lista usuários cadastrados."""
    try:
        limit = request.args.get("limit", 20, type=int)
        page_token = request.args.get("pageToken")

        usuarios = listar_usuarios(limit=limit, page_token=page_token)
        return usuarios

    except Exception as e:
        abort(500, message=f"Erro ao listar usuários: {str(e)}")


@user_bp.response(200, description="Dados do usuário")
@user_bp.route("/<user_id>", methods=["GET"])
def obter_usuario_endpoint(user_id):
    """Obtém dados de um usuário específico."""
    try:
        usuario = obter_usuario(user_id)
        if not usuario:
            abort(404, message="Usuário não encontrado")

        return usuario

    except Exception as e:
        abort(500, message=f"Erro ao obter usuário: {str(e)}")


@user_bp.response(200, description="Usuário atualizado com sucesso")
@user_bp.route("/<user_id>", methods=["PUT"])
def atualizar_usuario_endpoint(user_id):
    """Atualiza dados de um usuário."""
    try:
        user_data = request.get_json()
        atualizar_usuario(user_id, user_data)
        return {"message": "Usuário atualizado com sucesso"}
    except Exception as e:
        abort(500, message=f"Erro ao atualizar usuário: {str(e)}")


@user_bp.response(200, description="Usuário deletado com sucesso")
@user_bp.route("/<user_id>", methods=["DELETE"])
def deletar_usuario_endpoint(user_id):
    """Deleta um usuário."""
    try:
        deletar_usuario(user_id)
        return {"message": "Usuário deletado com sucesso"}

    except Exception as e:
        abort(500, message=f"Erro ao deletar usuário: {str(e)}")


@user_bp.response(200, description="Atividade registrada com sucesso")
@user_bp.route("/<user_id>/activity", methods=["POST"])
def registrar_atividade_endpoint(user_id):
    activity_data = request.get_json()
    try:
        registrar_atividade(
            user_id=user_id,
            tipo_atividade=activity_data["tipo"],
            dados_atividade=activity_data["dados"],
            duracao=activity_data.get("duracao")
        )
        return {"message": "Atividade registrada com sucesso"}
    except Exception as e:
        abort(500, message=f"Erro ao registrar atividade: {str(e)}")
