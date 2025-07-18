# flask_backend/services/flashcard_service.py
"""
Serviço para gerenciamento de flashcards com sistema de repetição espaçada.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from .base_service import BaseService
from ..utils import validate_required_fields, sanitize_string
from ..database import db


class FlashcardService(BaseService):
    """Serviço para operações com flashcards."""

    @property
    def collection_name(self) -> str:
        return "flashcards"

    def criar_flashcard(self, usuario_id: str, disciplina: str, topico: str,
                        subtopico: str, pergunta: str, resposta: str) -> str:
        """Cria um novo flashcard com configurações iniciais de repetição espaçada."""

        # Validações básicas
        required_fields = ["usuario_id", "disciplina",
                           "topico", "subtopico", "pergunta", "resposta"]
        data = {
            "usuario_id": usuario_id,
            "disciplina": disciplina,
            "topico": topico,
            "subtopico": subtopico,
            "pergunta": pergunta,
            "resposta": resposta
        }

        missing = validate_required_fields(data, required_fields)
        if missing:
            raise ValueError(
                f"Campos obrigatórios faltando: {', '.join(missing)}")

        # Sanitizar strings
        data.update({
            "disciplina": sanitize_string(disciplina),
            "topico": sanitize_string(topico),
            "subtopico": sanitize_string(subtopico),
            "pergunta": sanitize_string(pergunta),
            "resposta": sanitize_string(resposta)
        })

        # Configurações iniciais do algoritmo de repetição espaçada
        data.update({
            "intervalo": 1,  # dias iniciais
            "proxima_revisao": datetime.utcnow(),
            "acertos": 0,
            "erros": 0,
            "facilidade": 2.5,  # fator de facilidade inicial
            "revisoes": 0
        })

        return self.create(data)

    def listar_para_revisao(self, usuario_id: str, limit: int = 20,
                            start_after_id: Optional[str] = None) -> Dict[str, Any]:
        """Lista flashcards pendentes de revisão para um usuário."""
        agora = datetime.utcnow()

        query = (self.get_collection()
                 .where("usuario_id", "==", usuario_id)
                 .where("proxima_revisao", "<=", agora)
                 .order_by("proxima_revisao"))

        if start_after_id:
            last_doc = self.get_collection().document(start_after_id).get()
            if last_doc.exists:
                query = query.start_after(last_doc)

        docs = query.limit(limit).stream()
        items = []
        last_doc = None

        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            items.append(data)
            last_doc = doc

        # Próximo cursor para paginação
        next_page_token = None
        if len(items) == limit and last_doc:
            next_page_token = last_doc.id

        return {
            "items": items,
            "nextPageToken": next_page_token
        }

    def atualizar_revisao(self, card_id: str, acerto: bool) -> bool:
        """Atualiza estatísticas e agenda próxima revisão usando algoritmo SM-2 simplificado."""
        doc_ref = self.get_collection().document(card_id)
        doc = doc_ref.get()

        if not doc.exists:
            return False

        data = doc.to_dict()

        # Algoritmo de repetição espaçada simplificado (baseado no SM-2)
        intervalo_atual = data.get("intervalo", 1)
        facilidade = data.get("facilidade", 2.5)
        revisoes = data.get("revisoes", 0)

        if acerto:
            revisoes += 1
            if revisoes == 1:
                novo_intervalo = 1
            elif revisoes == 2:
                novo_intervalo = 6
            else:
                novo_intervalo = int(intervalo_atual * facilidade)

            # Ajustar facilidade (tornar mais fácil se acertou)
            facilidade = max(1.3, facilidade + 0.1)

            acertos = data.get("acertos", 0) + 1
            erros = data.get("erros", 0)
        else:
            # Erro: resetar intervalo e diminuir facilidade
            novo_intervalo = 1
            facilidade = max(1.3, facilidade - 0.2)
            revisoes = 0  # Resetar contador de revisões

            acertos = data.get("acertos", 0)
            erros = data.get("erros", 0) + 1

        # Calcular próxima revisão
        proxima_revisao = datetime.utcnow() + timedelta(days=novo_intervalo)

        # Atualizar documento
        doc_ref.update({
            "intervalo": novo_intervalo,
            "proxima_revisao": proxima_revisao,
            "acertos": acertos,
            "erros": erros,
            "facilidade": facilidade,
            "revisoes": revisoes,
            "ultima_revisao": datetime.utcnow()
        })

        return True

    def get_estatisticas_usuario(self, usuario_id: str) -> Dict[str, Any]:
        """Retorna estatísticas de estudo do usuário."""
        flashcards = self.find_by_field("usuario_id", usuario_id)

        total = len(flashcards)
        acertos_total = sum(f.get("acertos", 0) for f in flashcards)
        erros_total = sum(f.get("erros", 0) for f in flashcards)

        # Flashcards por disciplina
        disciplinas = {}
        for f in flashcards:
            disc = f.get("disciplina", "Sem disciplina")
            if disc not in disciplinas:
                disciplinas[disc] = {"total": 0, "acertos": 0, "erros": 0}
            disciplinas[disc]["total"] += 1
            disciplinas[disc]["acertos"] += f.get("acertos", 0)
            disciplinas[disc]["erros"] += f.get("erros", 0)

        # Flashcards pendentes de revisão
        agora = datetime.utcnow()
        pendentes = len([f for f in flashcards
                        if f.get("proxima_revisao", agora) <= agora])

        return {
            "total_flashcards": total,
            "acertos_total": acertos_total,
            "erros_total": erros_total,
            "taxa_acerto": round(acertos_total / max(acertos_total + erros_total, 1) * 100, 1),
            "pendentes_revisao": pendentes,
            "disciplinas": disciplinas
        }


# Instância singleton do serviço
flashcard_service = FlashcardService()

# Funções de compatibilidade (para não quebrar código existente)


def criar_flashcard(*args, **kwargs):
    return flashcard_service.criar_flashcard(*args, **kwargs)


def listar_para_revisao(*args, **kwargs):
    return flashcard_service.listar_para_revisao(*args, **kwargs)


def atualizar_revisao(*args, **kwargs):
    return flashcard_service.atualizar_revisao(*args, **kwargs)
