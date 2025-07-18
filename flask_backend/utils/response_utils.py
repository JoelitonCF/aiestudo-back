# flask_backend/utils/response_utils.py
"""
Utilitários para padronização de respostas da API.
"""
from typing import Dict, Any, Optional
from flask import jsonify


def success_response(data: Any = None, message: str = "Sucesso") -> Dict[str, Any]:
    """Resposta padronizada de sucesso."""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return response


def error_response(message: str = "Erro interno", code: int = 500, details: Optional[Dict] = None) -> tuple:
    """Resposta padronizada de erro."""
    response = {
        "success": False,
        "error": {
            "message": message,
            "code": code
        }
    }
    if details:
        response["error"]["details"] = details

    return jsonify(response), code


def validation_error_response(errors: Dict[str, Any]) -> tuple:
    """Resposta específica para erros de validação."""
    return error_response(
        message="Dados inválidos",
        code=422,
        details=errors
    )


def not_found_response(resource: str = "Recurso") -> tuple:
    """Resposta padronizada para recursos não encontrados."""
    return error_response(
        message=f"{resource} não encontrado",
        code=404
    )


def pagination_response(items: list, next_page_token: Optional[str] = None, total: Optional[int] = None) -> Dict[str, Any]:
    """Resposta padronizada para listagem com paginação."""
    response = {
        "items": items,
        "pagination": {
            "count": len(items),
            "nextPageToken": next_page_token
        }
    }

    if total is not None:
        response["pagination"]["total"] = total

    return response
