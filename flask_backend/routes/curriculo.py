# flask_backend/routes/curriculo.py


from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.schemas.curriculo_schema import CurriculoSchema
from flask_backend.schemas.id_schema import IdSchema
from flask_backend.schemas.curriculo_list_schema import CurriculoListSchema
from flask_backend.services import curriculo_service
from flask_backend.config import Config
from flask_backend.database import db

curriculo_bp = Blueprint(
    "curriculo",                   # nome interno
    "Curriculo",                   # tag no OpenAPI
    url_prefix="/api/v1/curriculos",
    description="Gerencia currículos"
)


@curriculo_bp.route("/", methods=["GET"])
@curriculo_bp.response(200, CurriculoListSchema)
def get_all_curriculos():
    """
    Lista currículos com paginação cursor-based.
    Query params opcionais: ?limit=<n>&pageToken=<cursor>
    """
    limit = int(request.args.get("limit", 20))
    page_token = request.args.get("pageToken")
    result = curriculo_service.listar_curriculos(limit, page_token)
    return result  # {"items":[{...}], "nextPageToken": "..."}


@curriculo_bp.route("/", methods=["POST"])
@curriculo_bp.arguments(CurriculoSchema)
@curriculo_bp.response(201, IdSchema)
def post_curriculo(payload):
    """
    Insere um novo currículo (flat no Firestore).
    Retorna o ID gerado.
    """
    doc_id = curriculo_service.inserir_curriculo(payload)
    return {"id": doc_id}


@curriculo_bp.route("/<concurso>/<cargo>", methods=["GET"])
@curriculo_bp.response(200, CurriculoSchema)
def get_curriculo(concurso, cargo):
    """
    Obtém um currículo específico. 404 se não existir.
    """
    curr = curriculo_service.obter_curriculo(concurso, cargo)
    if curr is None:
        abort(404, message="Currículo não encontrado")
    return curr


@curriculo_bp.route("/<concurso>/<cargo>", methods=["PUT"])
def update_curriculo(concurso, cargo):
    data = request.get_json() or {}
    doc_id = f"{concurso}_{cargo}".replace(" ", "")
    ref = db.collection(Config.FIRESTORE_COLLECTION).document(doc_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Currículo não encontrado"}), 404
    ref.update(data)
    return jsonify({"ok": True, "mensagem": "Currículo atualizado"})


@curriculo_bp.route("/<concurso>/<cargo>", methods=["DELETE"])
def delete_curriculo(concurso, cargo):
    doc_id = f"{concurso}_{cargo}".replace(" ", "")
    ref = db.collection(Config.FIRESTORE_COLLECTION).document(doc_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Currículo não encontrado"}), 404
    ref.delete()
    return jsonify({"ok": True, "mensagem": "Currículo removido"})
