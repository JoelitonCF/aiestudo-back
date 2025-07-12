from flask import request, jsonify
from flask_smorest import Blueprint
from flask_backend.services import openai_service
from flask_backend.database import db
from datetime import datetime

gerador_bp = Blueprint('gerador', __name__, url_prefix='/api/v1')


@gerador_bp.route("/gerar_conteudo", methods=["POST"])
def gerar_conteudo_completo_route():
    """
    Gera conteúdo completo: resumo, quiz e flashcards
    """
    payload = request.get_json() or {}
    
    # Validação dos campos obrigatórios
    disciplina = payload.get("disciplina")
    topico = payload.get("topico")
    usuario_id = payload.get("usuario_id", "usuario_teste")  # TODO: usar usuário real
    
    if not disciplina or not topico:
        return jsonify({
            "ok": False,
            "erro": "disciplina e topico são obrigatórios"
        }), 400
    
    # Campos opcionais
    nivel = payload.get("nivel", "intermediario")
    num_questoes = payload.get("num_questoes", 10)
    num_flashcards = payload.get("num_flashcards", 8)
    
    try:
        resultado = openai_service.gerar_conteudo_completo(
            disciplina=disciplina,
            topico=topico,
            nivel=nivel,
            num_questoes=num_questoes,
            num_flashcards=num_flashcards
        )
        
        if "erro" in resultado:
            return jsonify({
                "ok": False,
                "erro": resultado["erro"]
            }), 500
        
        # Salvar conteúdo no banco
        data_criacao = datetime.now().isoformat()
        
        # Salvar resumo
        resumo_data = {
            "usuario_id": usuario_id,
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "resumo": resultado["resumo"],
            "data_criacao": data_criacao,
            "tipo": "resumo"
        }
        resumo_ref = db.collection("conteudos_gerados").add(resumo_data)
        
        # Salvar quiz
        quiz_data = {
            "usuario_id": usuario_id,
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "questoes": resultado["quiz"],
            "data_criacao": data_criacao,
            "tipo": "quiz"
        }
        quiz_ref = db.collection("quizzes_gerados").add(quiz_data)
        
        # Salvar flashcards
        flashcards_data = {
            "usuario_id": usuario_id,
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "flashcards": resultado["flashcards"],
            "data_criacao": data_criacao,
            "tipo": "flashcards"
        }
        flashcards_ref = db.collection("flashcards_gerados").add(flashcards_data)
        
        return jsonify({
            "ok": True,
            "conteudo": resultado,
            "ids_salvos": {
                "resumo_id": resumo_ref[1].id,
                "quiz_id": quiz_ref[1].id,
                "flashcards_id": flashcards_ref[1].id
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": f"Erro interno: {str(e)}"
        }), 500


@gerador_bp.route("/gerar_resumo", methods=["POST"])
def gerar_resumo_route():
    """
    Gera apenas um resumo de estudo
    """
    payload = request.get_json() or {}
    
    disciplina = payload.get("disciplina")
    topico = payload.get("topico")
    usuario_id = payload.get("usuario_id", "usuario_teste")
    
    if not disciplina or not topico:
        return jsonify({
            "ok": False,
            "erro": "disciplina e topico são obrigatórios"
        }), 400
    
    nivel = payload.get("nivel", "intermediario")
    
    try:
        resultado = openai_service.gerar_resumo_estudo(
            disciplina=disciplina,
            topico=topico,
            nivel=nivel
        )
        
        if "erro" in resultado:
            return jsonify({
                "ok": False,
                "erro": resultado["erro"]
            }), 500
        
        # Salvar no banco
        data_criacao = datetime.now().isoformat()
        resumo_data = {
            "usuario_id": usuario_id,
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "resumo": resultado["resumo"],
            "data_criacao": data_criacao,
            "tipo": "resumo"
        }
        resumo_ref = db.collection("conteudos_gerados").add(resumo_data)
        
        return jsonify({
            "ok": True,
            "resumo": resultado,
            "id_salvo": resumo_ref[1].id
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": f"Erro interno: {str(e)}"
        }), 500


@gerador_bp.route("/gerar_quiz", methods=["POST"])
def gerar_quiz_route():
    """
    Gera apenas um quiz
    """
    payload = request.get_json() or {}
    
    disciplina = payload.get("disciplina")
    topico = payload.get("topico")
    usuario_id = payload.get("usuario_id", "usuario_teste")
    
    if not disciplina or not topico:
        return jsonify({
            "ok": False,
            "erro": "disciplina e topico são obrigatórios"
        }), 400
    
    nivel = payload.get("nivel", "intermediario")
    num_questoes = payload.get("num_questoes", 10)
    
    try:
        resultado = openai_service.gerar_quiz_ia(
            disciplina=disciplina,
            topico=topico,
            nivel=nivel,
            num_questoes=num_questoes
        )
        
        if "erro" in resultado:
            return jsonify({
                "ok": False,
                "erro": resultado["erro"]
            }), 500
        
        # Salvar no banco
        data_criacao = datetime.now().isoformat()
        quiz_data = {
            "usuario_id": usuario_id,
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "questoes": resultado["questoes"],
            "data_criacao": data_criacao,
            "tipo": "quiz"
        }
        quiz_ref = db.collection("quizzes_gerados").add(quiz_data)
        
        return jsonify({
            "ok": True,
            "quiz": resultado,
            "id_salvo": quiz_ref[1].id
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": f"Erro interno: {str(e)}"
        }), 500


@gerador_bp.route("/gerar_flashcards", methods=["POST"])
def gerar_flashcards_route():
    """
    Gera apenas flashcards
    """
    payload = request.get_json() or {}
    
    disciplina = payload.get("disciplina")
    topico = payload.get("topico")
    usuario_id = payload.get("usuario_id", "usuario_teste")
    
    if not disciplina or not topico:
        return jsonify({
            "ok": False,
            "erro": "disciplina e topico são obrigatórios"
        }), 400
    
    nivel = payload.get("nivel", "intermediario")
    num_flashcards = payload.get("num_flashcards", 8)
    
    try:
        resultado = openai_service.gerar_flashcards_ia(
            disciplina=disciplina,
            topico=topico,
            nivel=nivel,
            num_flashcards=num_flashcards
        )
        
        if "erro" in resultado:
            return jsonify({
                "ok": False,
                "erro": resultado["erro"]
            }), 500
        
        # Salvar no banco
        data_criacao = datetime.now().isoformat()
        flashcards_data = {
            "usuario_id": usuario_id,
            "disciplina": disciplina,
            "topico": topico,
            "nivel": nivel,
            "flashcards": resultado["flashcards"],
            "data_criacao": data_criacao,
            "tipo": "flashcards"
        }
        flashcards_ref = db.collection("flashcards_gerados").add(flashcards_data)
        
        return jsonify({
            "ok": True,
            "flashcards": resultado,
            "id_salvo": flashcards_ref[1].id
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": f"Erro interno: {str(e)}"
        }), 500


@gerador_bp.route("/conteudos_salvos", methods=["GET"])
def listar_conteudos_salvos():
    """
    Lista conteúdos salvos do usuário
    """
    usuario_id = request.args.get("usuario_id", "usuario_teste")
    disciplina = request.args.get("disciplina")
    tipo = request.args.get("tipo")  # resumo, quiz, flashcards
    
    try:
        query = db.collection("conteudos_gerados").where("usuario_id", "==", usuario_id)
        
        if disciplina:
            query = query.where("disciplina", "==", disciplina)
        if tipo:
            query = query.where("tipo", "==", tipo)
            
        docs = query.stream()
        conteudos = []
        
        for doc in docs:
            conteudo = doc.to_dict()
            conteudo["id"] = doc.id
            conteudos.append(conteudo)
        
        return jsonify({
            "ok": True,
            "conteudos": conteudos
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": f"Erro interno: {str(e)}"
        }), 500


@gerador_bp.route("/quizzes_salvos", methods=["GET"])
def listar_quizzes_salvos():
    """
    Lista quizzes salvos do usuário
    """
    usuario_id = request.args.get("usuario_id", "usuario_teste")
    disciplina = request.args.get("disciplina")
    
    try:
        query = db.collection("quizzes_gerados").where("usuario_id", "==", usuario_id)
        
        if disciplina:
            query = query.where("disciplina", "==", disciplina)
            
        docs = query.stream()
        quizzes = []
        
        for doc in docs:
            quiz = doc.to_dict()
            quiz["id"] = doc.id
            quizzes.append(quiz)
        
        return jsonify({
            "ok": True,
            "quizzes": quizzes
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": f"Erro interno: {str(e)}"
        }), 500


@gerador_bp.route("/flashcards_salvos", methods=["GET"])
def listar_flashcards_salvos():
    """
    Lista flashcards salvos do usuário
    """
    usuario_id = request.args.get("usuario_id", "usuario_teste")
    disciplina = request.args.get("disciplina")
    
    try:
        query = db.collection("flashcards_gerados").where("usuario_id", "==", usuario_id)
        
        if disciplina:
            query = query.where("disciplina", "==", disciplina)
            
        docs = query.stream()
        flashcards = []
        
        for doc in docs:
            flashcard = doc.to_dict()
            flashcard["id"] = doc.id
            flashcards.append(flashcard)
        
        return jsonify({
            "ok": True,
            "flashcards": flashcards
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "erro": f"Erro interno: {str(e)}"
        }), 500


@gerador_bp.route("/topicos_sugeridos", methods=["GET"])
def topicos_sugeridos_route():
    """
    Retorna uma lista de tópicos sugeridos para estudo
    """
    disciplina = request.args.get("disciplina")
    
    if not disciplina:
        return jsonify({
            "ok": False,
            "erro": "disciplina é obrigatória"
        }), 400
    
    # Tópicos sugeridos por disciplina (pode ser expandido)
    topicos_por_disciplina = {
        "matematica": [
            "Equações do 1º grau",
            "Equações do 2º grau",
            "Funções",
            "Geometria Plana",
            "Trigonometria",
            "Probabilidade",
            "Estatística"
        ],
        "portugues": [
            "Gramática",
            "Interpretação de Texto",
            "Redação",
            "Literatura",
            "Ortografia",
            "Pontuação",
            "Sintaxe"
        ],
        "direito": [
            "Direito Constitucional",
            "Direito Administrativo",
            "Direito Civil",
            "Direito Penal",
            "Direito Processual",
            "Direito do Trabalho",
            "Direito Tributário"
        ],
        "historia": [
            "História do Brasil",
            "História Geral",
            "História Contemporânea",
            "História Antiga",
            "História Medieval",
            "História Moderna"
        ],
        "geografia": [
            "Geografia Física",
            "Geografia Humana",
            "Geografia do Brasil",
            "Geografia Mundial",
            "Cartografia",
            "Climatologia"
        ]
    }
    
    topicos = topicos_por_disciplina.get(disciplina.lower(), [])
    
    return jsonify({
        "ok": True,
        "disciplina": disciplina,
        "topicos": topicos
    }), 200 