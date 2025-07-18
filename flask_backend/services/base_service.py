# flask_backend/services/base_service.py
"""
Classe base para serviços com operações CRUD comuns.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
from ..database import db


class BaseService(ABC):
    """Classe base para serviços com operações CRUD padronizadas."""

    @property
    @abstractmethod
    def collection_name(self) -> str:
        """Nome da coleção no Firestore."""
        pass

    def get_collection(self):
        """Retorna referência da coleção."""
        return db.collection(self.collection_name)

    def create(self, data: Dict[str, Any]) -> str:
        """Cria um novo documento e retorna o ID."""
        # Adiciona timestamp de criação
        if 'created_at' not in data:
            data['created_at'] = datetime.utcnow()

        _, ref = self.get_collection().add(data)
        return ref.id

    def get_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Busca documento por ID."""
        doc = self.get_collection().document(doc_id).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None

    def update(self, doc_id: str, data: Dict[str, Any]) -> bool:
        """Atualiza um documento existente."""
        # Adiciona timestamp de atualização
        data['updated_at'] = datetime.utcnow()

        doc_ref = self.get_collection().document(doc_id)
        if doc_ref.get().exists:
            doc_ref.update(data)
            return True
        return False

    def delete(self, doc_id: str) -> bool:
        """Remove um documento."""
        doc_ref = self.get_collection().document(doc_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False

    def list_all(self, limit: int = 50, start_after: Optional[str] = None) -> Dict[str, Any]:
        """Lista documentos com paginação."""
        query = self.get_collection().limit(limit)

        if start_after:
            # Busca documento para usar como cursor
            start_doc = self.get_collection().document(start_after).get()
            if start_doc.exists:
                query = query.start_after(start_doc)

        docs = query.stream()
        items = []
        last_doc = None

        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            items.append(data)
            last_doc = doc

        # Próximo cursor (se houver mais documentos)
        next_page_token = None
        if len(items) == limit and last_doc:
            next_page_token = last_doc.id

        return {
            "items": items,
            "nextPageToken": next_page_token
        }

    def find_by_field(self, field: str, value: Any, limit: int = 50) -> List[Dict[str, Any]]:
        """Busca documentos por um campo específico."""
        docs = self.get_collection().where(field, "==", value).limit(limit).stream()

        items = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            items.append(data)

        return items

    def count_by_field(self, field: str, value: Any) -> int:
        """Conta documentos que atendem um critério."""
        docs = self.get_collection().where(field, "==", value).stream()
        return len(list(docs))
