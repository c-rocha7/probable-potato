from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from typing import Dict, Any, Type
from django.db import models
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)


class BaseViewMixin:
    """Mixin com métodos comuns para views"""
    
    @staticmethod
    def validate_method(request, allowed_method: str) -> Response:
        """Valida se o método HTTP está correto"""
        if request.method != allowed_method:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return None
    
    @staticmethod
    def handle_exception(e: Exception, operation: str = "operação") -> Response:
        """Trata exceções de forma padronizada"""
        error_message = f"Erro durante {operation}: {str(e)}"
        logger.error(error_message)
        print(error_message)  # Manter print para compatibilidade
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def get_object_or_404_response(model: Type[models.Model], pk: Any) -> tuple:
        """Busca objeto ou retorna resposta 404"""
        try:
            obj = model.objects.get(pk=pk)
            return obj, None
        except model.DoesNotExist:
            error_message = f'{model.__name__} não encontrado'
            return None, Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def serialize_and_respond(obj, serializer_class: Type[serializers.Serializer], 
                            many: bool = False, status_code: int = status.HTTP_200_OK) -> Response:
        """Serializa objeto e retorna resposta"""
        serializer = serializer_class(obj, many=many)
        return Response(serializer.data, status=status_code)
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Response:
        """Valida se campos obrigatórios estão presentes"""
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            error_message = f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        return None


class APIResponseHandler:
    """Classe para padronizar respostas da API"""
    
    @staticmethod
    def success_response(data=None, message="Operação realizada com sucesso", 
                        status_code=status.HTTP_200_OK):
        """Resposta de sucesso padronizada"""
        response_data = {"success": True, "message": message}
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error_response(error_message, status_code=status.HTTP_400_BAD_REQUEST, 
                      error_code=None):
        """Resposta de erro padronizada"""
        response_data = {
            "success": False,
            "error": error_message
        }
        if error_code:
            response_data["error_code"] = error_code
        return Response(response_data, status=status_code)
    
    @staticmethod
    def not_found_response(resource_name="Recurso"):
        """Resposta 404 padronizada"""
        return APIResponseHandler.error_response(
            f"{resource_name} não encontrado",
            status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def validation_error_response(serializer):
        """Resposta de erro de validação padronizada"""
        return APIResponseHandler.error_response(
            "Dados inválidos",
            status.HTTP_400_BAD_REQUEST
        )
