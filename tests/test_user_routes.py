# tests/test_user_routes.py
import pytest

GET_U = '/api/v1/users/U1'
POST_U = '/api/v1/users'
ACT_U = '/api/v1/users/U1/activity'


def test_get_user_not_found(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.user_service.get_user',
        lambda uid: None
    )
    r = client.get(GET_U)
    assert r.status_code == 404


def test_get_user_success(client, monkeypatch):
    data = {"nome": "N", "xp": 0, "streak": 0}
    monkeypatch.setattr(
        'flask_backend.services.user_service.get_user',
        lambda uid: {**data, "last_activity": None}
    )
    r = client.get(GET_U)
    assert r.status_code == 200
    assert r.json["nome"] == "N"


def test_create_user_success(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.user_service.create_user',
        lambda uid, nome: {"user_id": uid, "nome": nome}
    )
    r = client.post(POST_U, json={"user_id": "U1", "nome": "N"})
    assert r.status_code == 201


def test_create_user_validation_error(client):
    r = client.post(POST_U, json={})
    assert r.status_code == 400


def test_add_activity_success(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.user_service.add_xp_and_update_streak',
        lambda uid, xp: {"xp": 10, "streak": 1}
    )
    r = client.post(ACT_U, json={"xp": 5})
    assert r.status_code == 200


def test_add_activity_not_found(client, monkeypatch):
    def fake(uid, xp): raise ValueError("não existe")
    monkeypatch.setattr(
        'flask_backend.services.user_service.add_xp_and_update_streak',
        fake
    )
    r = client.post(ACT_U, json={"xp": 5})
    assert r.status_code == 404
