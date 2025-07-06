# /app.py
from routes.plano import plano_bp
from routes.curriculo import curriculo_bp
from routes.desafio import desafio_bp
from routes.flashcard import fc_bp
from routes.user import user_bp
from routes.quiz import quiz_bp
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import DevelopmentConfig

load_dotenv()
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)


app.register_blueprint(desafio_bp, url_prefix="/api")
app.register_blueprint(curriculo_bp, url_prefix="/api")
app.register_blueprint(plano_bp, url_prefix="/api")
app.register_blueprint(fc_bp, url_prefix="/api")
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(quiz_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
