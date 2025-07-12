# flask_backend/routes/flashcard.py

from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask_backend.schemas.flashcard_schema import FlashcardSchema
from flask_backend.schemas.id_schema import IdSchema
from flask_backend.schemas.flashcard_review_schema import FlashcardReviewSchema
from flask_backend.schemas.simple_ok_schema import SimpleOkSchema
from flask_backend.services import flashcard_service
from flask_backend.database import db


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


@flashcard_bp.route("/", methods=["GET"])
def list_flashcards():
    user_id = request.args.get("user_id")
    flashcards = []
    query = db.collection("flashcards")
    if user_id:
        query = query.where("usuario_id", "==", user_id)
    docs = query.stream()
    for doc in docs:
        f = doc.to_dict()
        f["id"] = doc.id
        flashcards.append(f)
    return jsonify({"ok": True, "flashcards": flashcards})


@flashcard_bp.route("/<card_id>", methods=["GET"])
def get_flashcard(card_id):
    doc = db.collection("flashcards").document(card_id).get()
    if not doc.exists:
        return jsonify({"ok": False, "erro": "Flashcard não encontrado"}), 404
    flashcard = doc.to_dict()
    flashcard["id"] = doc.id
    return jsonify({"ok": True, "flashcard": flashcard})


@flashcard_bp.route("/<card_id>", methods=["PUT"])
def update_flashcard(card_id):
    data = request.get_json() or {}
    ref = db.collection("flashcards").document(card_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Flashcard não encontrado"}), 404
    ref.update(data)
    return jsonify({"ok": True, "mensagem": "Flashcard atualizado"})


@flashcard_bp.route("/<card_id>", methods=["DELETE"])
def delete_flashcard(card_id):
    ref = db.collection("flashcards").document(card_id)
    if not ref.get().exists:
        return jsonify({"ok": False, "erro": "Flashcard não encontrado"}), 404
    ref.delete()
    return jsonify({"ok": True, "mensagem": "Flashcard removido"})
