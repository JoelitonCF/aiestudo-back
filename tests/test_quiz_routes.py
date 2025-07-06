# tests/test_quiz_routes.py
import pytest

START = '/api/v1/quiz'
FINISH = '/api/v1/quiz/Q1/finish'


def test_post_quiz_success(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.quiz_service.start_quiz',
        lambda user, qs: 'QID'
    )
    r = client.post(START, json={"usuario_id": "U", "questoes": [{}]})
    assert r.status_code == 201
    assert r.json == {"quiz_id": "QID"}


@pytest.mark.parametrize("body", [{}, {"usuario_id": "U"}])
def test_post_quiz_validation_error(client, body):
    r = client.post(START, json=body)
    assert r.status_code == 400


def test_finish_quiz_success(client, monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.quiz_service.finish_quiz',
        lambda qid, resp: {"acertos": 1, "erros": 0, "tempo_total": 5}
    )
    r = client.post(FINISH, json={"respostas": {}})
    assert r.status_code == 200
    assert "acertos" in r.json


def test_finish_quiz_validation_error(client):
    r = client.post(FINISH, json={})
    assert r.status_code == 400


def test_finish_quiz_already_done(client, monkeypatch):
    def fake_fail(qid, resp):
        raise ValueError("já finalizado")
    monkeypatch.setattr(
        'flask_backend.services.quiz_service.finish_quiz',
        fake_fail
    )
    r = client.post(FINISH, json={"respostas": {}})
    assert r.status_code == 400
    assert "erro" in r.json
