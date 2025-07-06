# flask_backend/routes/flashcard.py

from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_backend.schemas.flashcard_schema import FlashcardSchema
from flask_backend.schemas.id_schema import IdSchema
from flask_backend.schemas.flashcard_review_schema import FlashcardReviewSchema
from flask_backend.schemas.simple_ok_schema import SimpleOkSchema
from flask_backend.services import flashcard_service

flashcard_bp = Blueprint(
    "flashcard",                # nome interno
    "Flashcard",                # tag no OpenAPI
    url_prefix="/api/v1/flashcards",
    description="Operações com flashcards"
)


@flashcard_bp.route("/", methods=["POST"])
# valida e desserializa o JSON de entrada
@flashcard_bp.arguments(FlashcardSchema)
# documenta que retorna { "id": "<string>" }
@flashcard_bp.response(201, IdSchema)
def post_flashcard(payload):
    """
    Cria um novo flashcard.
    """
    card_id = flashcard_service.criar_flashcard(**payload)
    return {"id": card_id}


@flashcard_bp.route("/revisao/<usuario_id>", methods=["GET"])
@flashcard_bp.response(200, FlashcardSchema(many=True))
def get_revisao(usuario_id):
    """
    Lista flashcards pendentes de revisão para um usuário.
    Query params opcionais: ?limit=<n>&pageToken=<cursor>
    """
    limit = int(request.args.get("limit", 20))
    page_token = request.args.get("pageToken")
    result = flashcard_service.listar_para_revisao(
        usuario_id, limit, page_token)
    # retorna só a lista de flashcards; o próximo cursor fica no campo result["nextPageToken"]
    return result["items"]


@flashcard_bp.route("/<card_id>/revisao", methods=["PATCH"])
# valida o { "acerto": true/false }
@flashcard_bp.arguments(FlashcardReviewSchema)
# documenta que retorna { "ok": true }
@flashcard_bp.response(200, SimpleOkSchema)
def patch_revisao(payload, card_id):
    """
    Atualiza os contadores de acertos/erros e agenda a próxima revisão.
    """
    acerto = payload["acerto"]
    try:
        flashcard_service.atualizar_revisao(card_id, acerto)
    except Exception as e:
        # aborta com 400 e mensagem de erro
        abort(400, message=str(e))
    return {"ok": True}
