# flask_backend/services/__init__.py
"""
Módulo de serviços - contém toda a lógica de negócio da aplicação.

Este módulo exporta instâncias prontas de todos os serviços para uso
nas rotas e outros módulos da aplicação.
"""

# Importar instâncias dos serviços
from .flashcard_service import flashcard_service
from .user_service import user_service
from .curriculo_service import curriculo_service
from .quiz_service import quiz_service

# Importar também as funções individuais para compatibilidade
from . import flashcard_service
from . import user_service
from . import curriculo_service
from . import quiz_service

# Exportar tudo para facilitar importação
__all__ = [
    # Instâncias dos serviços
    'flashcard_service',
    'user_service',
    'curriculo_service',
    'quiz_service',

    # Módulos individuais (para import específico se necessário)
    'flashcard_service',
    'user_service',
    'curriculo_service',
    'quiz_service'
]
