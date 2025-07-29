"""
Decorators personalizados para views
"""
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .services import ZapSignAPIException
from .mixins import APIResponseHandler
from .constants import ERROR_CODES
import logging

logger = logging.getLogger(__name__)


def handle_zapsign_exceptions(operation_name: str = "operação"):
    """
    Decorator para tratamento padronizado de exceções da API ZapSign
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            try:
                return view_func(*args, **kwargs)
            except ZapSignAPIException as e:
                logger.error(f"Erro na API ZapSign durante {operation_name}: {e.message}")
                return APIResponseHandler.error_response(
                    error_message=e.message,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error_code=ERROR_CODES['ZAPSIGN_API_ERROR']
                )
            except Exception as e:
                logger.error(f"Erro inesperado durante {operation_name}: {str(e)}")
                return APIResponseHandler.error_response(
                    error_message=f"Erro interno durante {operation_name}",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return wrapper
    return decorator


def validate_http_method(allowed_method: str):
    """
    Decorator para validação de método HTTP
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method != allowed_method:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_fields(required_fields: list):
    """
    Decorator para validação de campos obrigatórios
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            missing_fields = [
                field for field in required_fields 
                if field not in request.data or not request.data[field]
            ]
            if missing_fields:
                error_message = f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
                return APIResponseHandler.error_response(
                    error_message=error_message,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error_code=ERROR_CODES['VALIDATION_ERROR']
                )
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
