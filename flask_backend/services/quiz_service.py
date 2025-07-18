# flask_backend/services/quiz_service.py
"""
Serviço para gerenciamento de quizzes e avaliações.
"""
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid
import random

from .base_service import BaseService
from ..utils import validate_required_fields
from ..database import db
from flask_backend.services import openai_service


class QuizService(BaseService):
    """Serviço para operações com quizzes."""

    @property
    def collection_name(self) -> str:
        return "quizzes"

    def start_quiz(self, usuario_id, disciplina, subtopico=None, num_questoes=10, nivel="intermediario"):
        """Inicia um novo quiz."""
        quiz_id = str(uuid.uuid4())

        # Gerar questões usando OpenAI
        try:
            questoes = openai_service.gerar_questoes_quiz(
                disciplina=disciplina,
                subtopico=subtopico or "Geral",
                num_questoes=num_questoes,
                nivel=nivel
            )
        except Exception as e:
            # Fallback com questões básicas
            questoes = self._gerar_questoes_fallback(
                disciplina, subtopico, num_questoes)

        quiz_data = {
            "usuario_id": usuario_id,
            "disciplina": disciplina,
            "subtopico": subtopico,
            "num_questoes": num_questoes,
            "nivel": nivel,
            "questoes": questoes,
            "data_inicio": datetime.utcnow(),
            "status": "iniciado",
            "respostas": {},
            "pontuacao": None,
            "tempo_gasto": None
        }

        db.collection("quizzes").document(quiz_id).set(quiz_data)

        # Retornar apenas as questões sem as respostas corretas
        questoes_publicas = []
        for i, questao in enumerate(questoes):
            questoes_publicas.append({
                "id": i,
                "enunciado": questao["enunciado"],
                "alternativas": questao["alternativas"]
            })

        return {
            "quiz_id": quiz_id,
            "questoes": questoes_publicas,
            "tempo_limite": 30 * num_questoes  # 30 segundos por questão
        }

    def finish_quiz(self, quiz_id, respostas):
        """Finaliza um quiz e calcula o resultado."""
        doc = db.collection("quizzes").document(quiz_id).get()

        if not doc.exists:
            raise ValueError("Quiz não encontrado")

        quiz_data = doc.to_dict()

        if quiz_data["status"] != "iniciado":
            raise ValueError("Quiz já foi finalizado")

        # Calcular pontuação
        questoes = quiz_data["questoes"]
        pontuacao = 0
        detalhes = []

        for i, questao in enumerate(questoes):
            resposta_usuario = respostas.get(str(i))
            resposta_correta = questao["resposta_correta"]

            acertou = resposta_usuario == resposta_correta
            if acertou:
                pontuacao += 1

            detalhes.append({
                "questao": i,
                "resposta_usuario": resposta_usuario,
                "resposta_correta": resposta_correta,
                "acertou": acertou,
                "explicacao": questao.get("explicacao", "")
            })

        percentual = (pontuacao / len(questoes)) * 100
        tempo_gasto = (datetime.utcnow() -
                       quiz_data["data_inicio"]).total_seconds()

        resultado = {
            "pontuacao": pontuacao,
            "total_questoes": len(questoes),
            "percentual": round(percentual, 2),
            "detalhes": detalhes,
            "tempo_gasto": round(tempo_gasto),
            "status": "excelente" if percentual >= 80 else "bom" if percentual >= 60 else "precisa_melhorar"
        }

        # Atualizar quiz no banco
        db.collection("quizzes").document(quiz_id).update({
            "status": "finalizado",
            "data_fim": datetime.utcnow(),
            "respostas": respostas,
            "resultado": resultado,
            "tempo_gasto": tempo_gasto
        })

        return resultado

    def get_quiz_results(self, quiz_id: str) -> Dict[str, Any]:
        """Retorna resultados detalhados do quiz."""
        quiz = self.get_by_id(quiz_id)
        if not quiz:
            raise ValueError("Quiz não encontrado")

        if quiz.get("status") != "finalizado":
            raise ValueError("Quiz ainda não foi finalizado")

        # Análise por questão
        questoes_analise = []
        for i, questao in enumerate(quiz["questoes"]):
            analise = {
                "numero": i + 1,
                "pergunta": questao["pergunta"],
                "resposta_correta": questao["resposta_correta"],
                "resposta_usuario": questao.get("resposta_usuario"),
                "acertou": questao.get("acertou", False),
                "opcoes": questao["opcoes"]
            }
            questoes_analise.append(analise)

        return {
            "quiz_id": quiz_id,
            "usuario_id": quiz["usuario_id"],
            "tipo": quiz.get("tipo", "geral"),
            "disciplina": quiz.get("disciplina"),
            "acertos": quiz["acertos"],
            "erros": quiz["erros"],
            "total_questoes": quiz["total_questoes"],
            "score": quiz["score"],
            "tempo_total": quiz["tempo_total"],
            "started_at": quiz["started_at"],
            "finished_at": quiz["finished_at"],
            "questoes_detalhadas": questoes_analise
        }

    def get_user_quiz_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna histórico de quizzes do usuário."""
        quizzes = self.find_by_field("usuario_id", user_id, limit=limit)

        # Ordenar por data (mais recente primeiro)
        quizzes.sort(key=lambda x: x.get(
            "started_at", datetime.min), reverse=True)

        # Resumo dos quizzes
        quiz_summary = []
        for quiz in quizzes:
            summary = {
                "id": quiz.get("id"),
                "tipo": quiz.get("tipo", "geral"),
                "disciplina": quiz.get("disciplina"),
                "score": quiz.get("score", 0),
                "acertos": quiz.get("acertos", 0),
                "total_questoes": quiz.get("total_questoes", 0),
                "tempo_total": quiz.get("tempo_total"),
                "started_at": quiz.get("started_at"),
                "status": quiz.get("status", "em_andamento")
            }
            quiz_summary.append(summary)

        return quiz_summary

    def listar_quizzes_usuario(usuario_id):
        """Lista quizzes de um usuário."""
        docs = db.collection("quizzes").where("usuario_id", "==", usuario_id).order_by(
            "data_inicio", direction="DESCENDING").limit(20).stream()

        quizzes = []
        for doc in docs:
            quiz = doc.to_dict()
            quiz["id"] = doc.id

            # Remover questões dos resultados para economizar dados
            if "questoes" in quiz:
                del quiz["questoes"]

            quizzes.append(quiz)

        return quizzes

    def listar_quizzes_publicos():
        """Lista quizzes públicos/templates disponíveis."""
        return {
            "templates": [
                {
                    "id": "portugues_basico",
                    "titulo": "Português Básico",
                    "disciplina": "Língua Portuguesa",
                    "nivel": "basico",
                    "num_questoes": 10
                },
                {
                    "id": "direito_constitucional",
                    "titulo": "Direito Constitucional",
                    "disciplina": "Direito Constitucional",
                    "nivel": "intermediario",
                    "num_questoes": 15
                },
                {
                    "id": "matematica_avancada",
                    "titulo": "Matemática Avançada",
                    "disciplina": "Matemática",
                    "nivel": "avancado",
                    "num_questoes": 20
                }
            ]
        }

    def obter_quiz(quiz_id):
        """Obtém detalhes de um quiz específico."""
        doc = db.collection("quizzes").document(quiz_id).get()

        if not doc.exists:
            return None

        quiz = doc.to_dict()
        quiz["id"] = doc.id

        # Se o quiz ainda está em andamento, não mostrar respostas corretas
        if quiz["status"] == "iniciado" and "questoes" in quiz:
            questoes_sem_resposta = []
            for i, questao in enumerate(quiz["questoes"]):
                questoes_sem_resposta.append({
                    "id": i,
                    "enunciado": questao["enunciado"],
                    "alternativas": questao["alternativas"]
                })
            quiz["questoes"] = questoes_sem_resposta

        return quiz

    def deletar_quiz(quiz_id):
        """Deleta um quiz."""
        db.collection("quizzes").document(quiz_id).delete()

    def obter_estatisticas_usuario(usuario_id):
        """Obtém estatísticas de quiz de um usuário."""
        docs = db.collection("quizzes").where("usuario_id", "==", usuario_id).where(
            "status", "==", "finalizado").stream()

        total_quizzes = 0
        pontuacao_total = 0
        questoes_total = 0
        tempo_total = 0

        for doc in docs:
            quiz = doc.to_dict()
            if "resultado" in quiz:
                total_quizzes += 1
                pontuacao_total += quiz["resultado"]["pontuacao"]
                questoes_total += quiz["resultado"]["total_questoes"]
                tempo_total += quiz.get("tempo_gasto", 0)

        if total_quizzes == 0:
            return {"message": "Nenhum quiz finalizado encontrado"}

        return {
            "total_quizzes": total_quizzes,
            "media_acertos": round((pontuacao_total / questoes_total) * 100, 2),
            "tempo_medio": round(tempo_total / total_quizzes),
            "total_questoes": questoes_total
        }

    def _gerar_questoes_fallback(disciplina, subtopico, num_questoes):
        """Gera questões básicas caso a OpenAI falhe."""
        questoes = []

        for i in range(num_questoes):
            questoes.append({
                "enunciado": f"Questão {i+1} sobre {subtopico or disciplina}",
                "alternativas": [
                    "A) Primeira alternativa",
                    "B) Segunda alternativa",
                    "C) Terceira alternativa",
                    "D) Quarta alternativa",
                    "E) Quinta alternativa"
                ],
                "resposta_correta": random.choice(["A", "B", "C", "D", "E"]),
                "explicacao": "Esta é uma questão de exemplo. Consulte material específico da disciplina."
            })

        return questoes


# Instância singleton do serviço
quiz_service = QuizService()

# Funções de compatibilidade (para não quebrar código existente)


def start_quiz(*args, **kwargs):
    return quiz_service.start_quiz(*args, **kwargs)


def finish_quiz(*args, **kwargs):
    return quiz_service.finish_quiz(*args, **kwargs)
