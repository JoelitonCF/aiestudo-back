# tests/conftest.py

from flask_backend import create_app
import pytest
import os
import sys

# 1) Adiciona o diretório pai (app-myclass/) ao path, antes de tudo
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# 2) Agora sim importamos o create_app do seu pacote


@pytest.fixture
def app():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
