# flask_backend/utils/validation_utils.py
"""
Utilitários para validações comuns.
"""
import re
from typing import Dict, Any, List, Optional


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """Valida se campos obrigatórios estão presentes."""
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    return missing_fields


def validate_string_length(value: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """Valida comprimento de string."""
    return min_length <= len(value.strip()) <= max_length


def validate_email(email: str) -> bool:
    """Valida formato de email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_user_id(user_id: str) -> bool:
    """Valida formato de ID de usuário."""
    # Deve ter entre 3 e 50 caracteres, apenas alfanuméricos e alguns especiais
    pattern = r'^[a-zA-Z0-9._-]{3,50}$'
    return re.match(pattern, user_id) is not None


def sanitize_string(value: str) -> str:
    """Remove espaços extras e caracteres especiais perigosos."""
    return re.sub(r'[<>"]', '', value.strip())


def validate_positive_integer(value: Any) -> bool:
    """Valida se é um número inteiro positivo."""
    try:
        num = int(value)
        return num > 0
    except (ValueError, TypeError):
        return False


def validate_pagination_params(limit: Any, page_token: Any) -> Dict[str, Any]:
    """Valida parâmetros de paginação."""
    errors = {}

    # Validar limit
    try:
        limit = int(limit) if limit else 20
        if limit < 1 or limit > 100:
            errors['limit'] = 'Deve estar entre 1 e 100'
    except (ValueError, TypeError):
        errors['limit'] = 'Deve ser um número inteiro'
        limit = 20

    # Validar page_token (se fornecido)
    if page_token and not isinstance(page_token, str):
        errors['pageToken'] = 'Deve ser uma string'
        page_token = None

    return {
        'limit': limit,
        'page_token': page_token,
        'errors': errors
    }
