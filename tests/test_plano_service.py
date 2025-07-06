# tests/test_plano_service.py
from datetime import date, timedelta
import pytest
from flask_backend.services.plano_service import gerar_plano
from flask_backend.services.curriculo_service import obter_curriculo


def test_gerar_plano_no_curriculo(monkeypatch):
    monkeypatch.setattr(
        'flask_backend.services.curriculo_service.obter_curriculo', lambda c, g: None)
    assert gerar_plano("C", "G", 5) is None


def test_gerar_plano_basic(monkeypatch):
    # currículo com 1 disciplina e 2 subtopicos
    curr = {
        "disciplinas": {
            "D1": {
                "nome": "Disc",
                "T1": {"titulo": "Top", "descricao": ["s1", "s2"]},
                "T2": "SóTop"
            }
        }
    }
    monkeypatch.setattr(
        'flask_backend.services.curriculo_service.obter_curriculo',
        lambda c, g: curr
    )
    plano = gerar_plano("C", "G", dias=2)
    assert plano["concurso"] == "C"
    assert plano["cargo"] == "G"
    assert len(plano["plano"]) <= 2
    # deve conter itens com disciplina e subtopico
    assert all(
        "disciplina" in item for day in plano["plano"] for item in day["itens"])
