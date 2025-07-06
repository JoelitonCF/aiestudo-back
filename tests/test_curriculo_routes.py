# tests/test_curriculo_routes.py
import pytest

BASE = '/api/v1/curriculo'


def test_get_all_curriculos_empty(client, monkeypatch):
    # mockar listar_curriculos
    monkeypatch.setattr(
        'flask_backend.services.curriculo_service.listar_curriculos',
        lambda limit, token: {"items": [], "nextPageToken": None}
    )
    r = client.get(f'{BASE}?limit=5')
    assert r.status_code == 200
    assert r.json == {"items": [], "nextPageToken": None}


def test_post_curriculo_success(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.curriculo_service.inserir_curriculo',
        lambda payload: 'doc123'
    )
    payload = {"concurso": "X", "cargo": "Y"}
    r = client.post(BASE, json=payload)
    assert r.status_code == 201
    assert r.json == {"id": "doc123"}


def test_post_curriculo_validation_error(client):
    # sem concurso/cargo
    r = client.post(BASE, json={})
    assert r.status_code == 400
    assert 'erros' in r.json
