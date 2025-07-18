# flask_backend/utils/__init__.py
"""
Utilitários comuns para o backend.
"""
from .response_utils import (
    success_response,
    error_response,
    validation_error_response,
    not_found_response,
    pagination_response
)
from .validation_utils import (
    validate_required_fields,
    validate_string_length,
    validate_email,
    validate_user_id,
    sanitize_string,
    validate_positive_integer,
    validate_pagination_params
)

__all__ = [
    'success_response',
    'error_response',
    'validation_error_response',
    'not_found_response',
    'pagination_response',
    'validate_required_fields',
    'validate_string_length',
    'validate_email',
    'validate_user_id',
    'sanitize_string',
    'validate_positive_integer',
    'validate_pagination_params'
]
