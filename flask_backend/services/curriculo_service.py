
# flask_backend/services/curriculo_service.py
"""
Serviço para gerenciamento de currículos de concursos.
"""
from typing import Dict, Any, List, Optional

from .base_service import BaseService
from ..utils import validate_required_fields, sanitize_string
from ..config import Config
from ..database import db


class CurriculoService(BaseService):
    """Serviço para operações com currículos."""

    @property
    def collection_name(self) -> str:
        return Config.FIRESTORE_COLLECTION  # ex: "curriculos"

    def listar_curriculos(self, limit: int = 20, start_after_id: Optional[str] = None) -> Dict[str, Any]:
        """Lista currículos com paginação."""
        query = self.get_collection().order_by("concurso")

        if start_after_id:
            last_doc = self.get_collection().document(start_after_id).get()
            if last_doc.exists:
                query = query.start_after(last_doc)

        docs = query.limit(limit).stream()
        items = []
        last_doc = None

        for doc in docs:
            data = doc.to_dict()
            items.append({
                "id": doc.id,
                "concurso": data.get("concurso", ""),
                "cargo": data.get("cargo", ""),
                "disciplinas": len(data.get("disciplinas", [])),
                "total_topicos": self._count_total_topics(data.get("disciplinas", []))
            })
            last_doc = doc

        next_page_token = None
        if len(items) == limit and last_doc:
            next_page_token = last_doc.id

        return {
            "items": items,
            "nextPageToken": next_page_token
        }

    def obter_curriculo(self, concurso: str, cargo: str) -> Optional[Dict[str, Any]]:
        """Busca currículo específico por concurso e cargo."""
        if not concurso or not cargo:
            raise ValueError("Concurso e cargo são obrigatórios")

        doc_id = self._generate_curriculo_id(concurso, cargo)
        curriculo = self.get_by_id(doc_id)

        if curriculo:
            curriculo["id"] = doc_id
            # Adicionar metadados úteis
            curriculo["total_disciplinas"] = len(
                curriculo.get("disciplinas", []))
            curriculo["total_topicos"] = self._count_total_topics(
                curriculo.get("disciplinas", []))

        return curriculo

    def inserir_curriculo(self, curriculo_data: Dict[str, Any]) -> str:
        """Insere ou atualiza um currículo."""

        # Validar campos obrigatórios
        required_fields = ["concurso", "cargo", "disciplinas"]
        missing = validate_required_fields(curriculo_data, required_fields)
        if missing:
            raise ValueError(
                f"Campos obrigatórios faltando: {', '.join(missing)}")

        # Sanitizar strings
        curriculo_data["concurso"] = sanitize_string(
            curriculo_data["concurso"])
        curriculo_data["cargo"] = sanitize_string(curriculo_data["cargo"])

        # Validar estrutura das disciplinas
        if not isinstance(curriculo_data["disciplinas"], list):
            raise ValueError("'disciplinas' deve ser uma lista")

        for i, disciplina in enumerate(curriculo_data["disciplinas"]):
            if not isinstance(disciplina, dict):
                raise ValueError(f"Disciplina {i} deve ser um objeto")
            if "nome" not in disciplina:
                raise ValueError(f"Disciplina {i} deve ter um campo 'nome'")
            disciplina["nome"] = sanitize_string(disciplina["nome"])

        # Gerar ID do documento
        doc_id = self._generate_curriculo_id(
            curriculo_data["concurso"], curriculo_data["cargo"])

        # Adicionar metadados
        curriculo_data.update({
            "created_at": self._get_current_time(),
            "updated_at": self._get_current_time(),
            "total_disciplinas": len(curriculo_data["disciplinas"]),
            "total_topicos": self._count_total_topics(curriculo_data["disciplinas"])
        })

        # Salvar usando ID específico
        doc_ref = self.get_collection().document(doc_id)
        doc_ref.set(curriculo_data)

        return doc_id

    def buscar_por_disciplina(self, disciplina: str) -> List[Dict[str, Any]]:
        """Busca currículos que contenham uma disciplina específica."""
        disciplina = sanitize_string(disciplina).lower()

        # Como Firestore não suporta busca em arrays de objetos facilmente,
        # vamos buscar todos e filtrar no código
        all_curriculos = self.get_all()
        matching_curriculos = []

        for curriculo in all_curriculos:
            disciplinas = curriculo.get("disciplinas", [])
            for disc in disciplinas:
                if disciplina in disc.get("nome", "").lower():
                    matching_curriculos.append({
                        "id": curriculo.get("id"),
                        "concurso": curriculo.get("concurso"),
                        "cargo": curriculo.get("cargo"),
                        "disciplina_encontrada": disc.get("nome")
                    })
                    break

        return matching_curriculos

    def _generate_curriculo_id(self, concurso: str, cargo: str) -> str:
        """Gera ID único para o currículo baseado em concurso e cargo."""
        return f"{concurso}_{cargo}".replace(" ", "_").replace("/", "_").lower()

    def _count_total_topics(self, disciplinas: List[Dict]) -> int:
        """Conta o total de tópicos em todas as disciplinas."""
        total = 0
        for disciplina in disciplinas:
            topicos = disciplina.get("topicos", [])
            total += len(topicos)
        return total


# Instância singleton do serviço
curriculo_service = CurriculoService()

# Funções de compatibilidade (para não quebrar código existente)


def listar_curriculos(*args, **kwargs):
    return curriculo_service.listar_curriculos(*args, **kwargs)


def obter_curriculo(*args, **kwargs):
    return curriculo_service.obter_curriculo(*args, **kwargs)


def inserir_curriculo(*args, **kwargs):
    return curriculo_service.inserir_curriculo(*args, **kwargs)
