# flask_backend/services/user_service.py
"""
Serviço para gerenciamento de usuários e sistema de gamificação.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import uuid

from .base_service import BaseService
from ..utils import validate_required_fields, sanitize_string
from ..database import db


# Mock simples para testar sem Firebase - SEM IMPORTS DO FLASK

def criar_usuario(nome, email, concurso_foco=None, cargo_foco=None):
    """Cria um novo usuário no Firestore."""
    return user_service.create_user(nome, email, concurso_foco, cargo_foco)


def registrar_atividade(user_id, tipo_atividade, dados_atividade, duracao=None):
    atividade = {
        "tipo": tipo_atividade,
        "dados": dados_atividade,
        "duracao": duracao,
        "data": datetime.utcnow()
    }
    db.collection("users").document(user_id).collection("atividades").add(atividade)
    print(f"✅ Atividade registrada no Firestore: {user_id} - {tipo_atividade} - {duracao}min")
    return True


class UserService(BaseService):
    """Serviço para operações com usuários."""

    @property
    def collection_name(self) -> str:
        return "users"

    def create_user(self, nome: str, email: str, concurso_foco=None, cargo_foco=None) -> str:
        """Cria um novo usuário com configurações iniciais."""

        # Validações
        if not nome or not email:
            raise ValueError("Nome e email são obrigatórios")

        nome = sanitize_string(nome)
        if len(nome) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")

        # Gerar um ID de usuário único
        user_id = str(uuid.uuid4())

        usuario_data = {
            "nome": nome,
            "email": email,
            "concurso_foco": concurso_foco,
            "cargo_foco": cargo_foco,
            "data_criacao": datetime.utcnow(),
            "ativo": True,
            "xp": 0,
            "streak": 0,
            "last_activity": None,
            "created_at": datetime.utcnow(),
            "nivel": 1,
            "total_flashcards": 0,
            "total_acertos": 0,
            "total_erros": 0
        }

        # Usar o user_id como document ID
        doc_ref = self.get_collection().document(user_id)
        doc_ref.set(usuario_data)

        return user_id

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por ID."""
        user = self.get_by_id(user_id)
        if user:
            user["id"] = user_id
        return user

    def add_xp_and_update_streak(self, user_id: str, xp_earned: int) -> Dict[str, Any]:
        """Adiciona XP e atualiza streak do usuário."""
        if xp_earned < 0:
            raise ValueError("XP deve ser um valor positivo")

        doc_ref = self.get_collection().document(user_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise ValueError("Usuário não encontrado")

        user_data = doc.to_dict()
        now = datetime.utcnow()
        last_activity = user_data.get("last_activity")
        current_streak = user_data.get("streak", 0)

        # Calcular novo streak
        new_streak = self._calculate_streak(last_activity, current_streak, now)

        # Calcular novo XP e nível
        current_xp = user_data.get("xp", 0)
        new_xp = current_xp + xp_earned
        new_level = self._calculate_level(new_xp)

        # Atualizar dados
        update_data = {
            "xp": new_xp,
            "streak": new_streak,
            "last_activity": now,
            "nivel": new_level
        }

        doc_ref.update(update_data)

        return {
            "xp": new_xp,
            "streak": new_streak,
            "nivel": new_level,
            "xp_gained": xp_earned
        }

    def _calculate_streak(self, last_activity: Optional[datetime],
                          current_streak: int, now: datetime) -> int:
        """Calcula o novo streak baseado na última atividade."""
        if not last_activity:
            return 1

        delta = now.date() - last_activity.date()

        if delta == timedelta(days=0):
            # Mesma data, mantém streak
            return current_streak
        elif delta == timedelta(days=1):
            # Atividade consecutiva, incrementa
            return current_streak + 1
        else:
            # Quebrou o streak, recomeça
            return 1

    def _calculate_level(self, xp: int) -> int:
        """Calcula o nível baseado no XP total."""
        # Sistema de progressão: 100 XP para nível 2, 300 para nível 3, etc.
        if xp < 100:
            return 1
        elif xp < 300:
            return 2
        elif xp < 600:
            return 3
        elif xp < 1000:
            return 4
        else:
            return 5 + (xp - 1000) // 500  # 500 XP por nível após nível 5

    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Retorna estatísticas completas do usuário."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("Usuário não encontrado")

        # Calcular XP para próximo nível
        current_xp = user.get("xp", 0)
        current_level = user.get("nivel", 1)

        if current_level == 1:
            xp_for_next = 100 - current_xp
        elif current_level == 2:
            xp_for_next = 300 - current_xp
        elif current_level == 3:
            xp_for_next = 600 - current_xp
        elif current_level == 4:
            xp_for_next = 1000 - current_xp
        else:
            next_level_xp = 1000 + (current_level - 4) * 500
            xp_for_next = next_level_xp - current_xp

        return {
            "id": user_id,
            "nome": user.get("nome"),
            "xp": current_xp,
            "nivel": current_level,
            "streak": user.get("streak", 0),
            "xp_para_proximo_nivel": max(0, xp_for_next),
            "last_activity": user.get("last_activity"),
            "created_at": user.get("created_at"),
            "total_flashcards": user.get("total_flashcards", 0),
            "total_acertos": user.get("total_acertos", 0),
            "total_erros": user.get("total_erros", 0)
        }


# Instância singleton do serviço
user_service = UserService()

# Funções de compatibilidade (para não quebrar código existente)


def get_user(*args, **kwargs):
    return user_service.get_user(*args, **kwargs)


def create_user(*args, **kwargs):
    return user_service.create_user(*args, **kwargs)


def add_xp_and_update_streak(*args, **kwargs):
    return user_service.add_xp_and_update_streak(*args, **kwargs)


# Wrappers para manter compatibilidade, agora usando Firestore

def listar_usuarios(limit=20, page_token=None):
    return user_service.list_all(limit=limit)

def obter_usuario(user_id):
    return user_service.get_user(user_id)

def atualizar_usuario(user_id, dados):
    return user_service.update(user_id, dados)

def deletar_usuario(user_id):
    return user_service.delete(user_id)
