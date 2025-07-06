# tests/test_flashcard_routes.py
ITEM_ROUTE = '/api/v1/flashcards'
REV_ROUTE = '/api/v1/flashcards/revisao/USER1'
PATCH_ROUTE = '/api/v1/flashcards/ID123/revisao'


def test_post_flashcard_success(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.flashcard_service.criar_flashcard',
        lambda **kw: 'card123'
    )
    payload = {
        "usuario_id": "USER1", "disciplina": "D", "topico": "T",
        "subtopico": "S", "pergunta": "P?", "resposta": "R"
    }
    r = client.post(ITEM_ROUTE, json=payload)
    assert r.status_code == 201
    assert r.json == {"id": "card123"}


def test_post_flashcard_validation_error(client):
    r = client.post(ITEM_ROUTE, json={})
    assert r.status_code == 400
    assert 'erros' in r.json


def test_get_revisao(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.flashcard_service.listar_para_revisao',
        lambda user, limit=20, start=None: {
            "items": [{"id": "1"}], "nextPageToken": None}
    )
    r = client.get(REV_ROUTE + '?limit=1')
    assert r.status_code == 200
    assert r.json["items"][0]["id"] == "1"


def test_patch_revisao_success(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.flashcard_service.atualizar_revisao',
        lambda card_id, acerto: True
    )
    r = client.patch(PATCH_ROUTE, json={"acerto": True})
    assert r.status_code == 200
    assert r.json == {"ok": True}


def test_patch_revisao_validation_error(client):
    r = client.patch(PATCH_ROUTE, json={})
    assert r.status_code == 400
    assert 'erros' in r.json or 'erro' in r.json
