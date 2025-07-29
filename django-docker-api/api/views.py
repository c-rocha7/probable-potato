from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import Documento, Signatario
from .serializers import (
    DocumentoSerializer, 
    DocumentoWithSignersSerializer, 
    DocumentoUpdateSerializer, 
    SignatarioSerializer
)
from .services import ZapSignService, DocumentoService, ZapSignAPIException
from .mixins import BaseViewMixin, APIResponseHandler
from .constants import HTTP_METHODS, MESSAGES, ERROR_CODES

import logging

logger = logging.getLogger(__name__)


@api_view([HTTP_METHODS['GET']])
def get_documentos(request):
    """Retorna lista de todos os documentos"""
    method_error = BaseViewMixin.validate_method(request, HTTP_METHODS['GET'])
    if method_error:
        return method_error

    try:
        documentos = Documento.objects.all()
        return BaseViewMixin.serialize_and_respond(
            documentos, 
            DocumentoWithSignersSerializer, 
            many=True
        )
    except Exception as e:
        return BaseViewMixin.handle_exception(e, "busca de documentos")


@api_view([HTTP_METHODS['GET']])
def get_documento(request, pk):
    """Retorna um documento específico por ID"""
    method_error = BaseViewMixin.validate_method(request, HTTP_METHODS['GET'])
    if method_error:
        return method_error

    documento, error_response = BaseViewMixin.get_object_or_404_response(Documento, pk)
    if error_response:
        return error_response

    try:
        return BaseViewMixin.serialize_and_respond(documento, DocumentoWithSignersSerializer)
    except Exception as e:
        return BaseViewMixin.handle_exception(e, "busca de documento")


@api_view([HTTP_METHODS['POST']])
def create_documento(request):
    """Cria um novo documento"""
    method_error = BaseViewMixin.validate_method(request, HTTP_METHODS['POST'])
    if method_error:
        return method_error

    # Validar campos obrigatórios
    required_fields = ['name', 'url_documento', 'nome_signatario', 'email_signatario']
    validation_error = BaseViewMixin.validate_required_fields(request.data, required_fields)
    if validation_error:
        return validation_error

    try:
        with transaction.atomic():
            # Usar services para interação com API externa
            zapsign_service = ZapSignService()
            documento_service = DocumentoService()
            
            # Criar documento na API ZapSign
            api_result = zapsign_service.create_document(request.data)
            
            # Preparar dados para salvar no banco
            document_data = documento_service.prepare_document_data(api_result, request.data)
            
            # Salvar documento no banco
            serializer = DocumentoSerializer(data=document_data)
            if not serializer.is_valid():
                logger.error(f"Erro de validação do documento: {serializer.errors}")
                return APIResponseHandler.validation_error_response(serializer)
            
            documento_criado = serializer.save()
            
            # Preparar e salvar signatário
            signer_data = documento_service.prepare_signer_data(
                api_result, request.data, documento_criado.id
            )
            
            signatario_serializer = SignatarioSerializer(data=signer_data)
            if signatario_serializer.is_valid():
                signatario_serializer.save()
                logger.info(f"Signatário cadastrado: {request.data.get('nome_signatario')}")
            else:
                logger.error(f"Erro ao cadastrar signatário: {signatario_serializer.errors}")

            return APIResponseHandler.success_response(
                data=serializer.data,
                message=MESSAGES['DOCUMENT_CREATED'],
                status_code=status.HTTP_201_CREATED
            )

    except ZapSignAPIException as e:
        logger.error(f"Erro na API ZapSign: {e.message}")
        return APIResponseHandler.error_response(
            error_message=e.message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ERROR_CODES['ZAPSIGN_API_ERROR']
        )
    except Exception as e:
        return BaseViewMixin.handle_exception(e, "criação de documento")


@api_view([HTTP_METHODS['PUT']])
def update_documento(request, pk):
    """Atualiza um documento existente"""
    method_error = BaseViewMixin.validate_method(request, HTTP_METHODS['PUT'])
    if method_error:
        return method_error

    documento, error_response = BaseViewMixin.get_object_or_404_response(Documento, pk)
    if error_response:
        return error_response

    # Validar campos obrigatórios
    validation_error = BaseViewMixin.validate_required_fields(request.data, ['name'])
    if validation_error:
        return validation_error

    try:
        # Usar service para interação com API externa
        zapsign_service = ZapSignService()
        
        # Atualizar documento na API ZapSign
        zapsign_service.update_document(documento.token, request.data)
        
        # Atualizar documento no banco local
        documento.name = request.data.get("name")
        documento.save()

        return BaseViewMixin.serialize_and_respond(
            documento, 
            DocumentoUpdateSerializer,
            status_code=status.HTTP_200_OK
        )

    except ZapSignAPIException as e:
        logger.error(f"Erro na API ZapSign: {e.message}")
        return APIResponseHandler.error_response(
            error_message=e.message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ERROR_CODES['ZAPSIGN_API_ERROR']
        )
    except Exception as e:
        return BaseViewMixin.handle_exception(e, "atualização de documento")


@api_view([HTTP_METHODS['DELETE']])
def delete_documento(request, pk):
    """Deleta um documento existente"""
    method_error = BaseViewMixin.validate_method(request, HTTP_METHODS['DELETE'])
    if method_error:
        return method_error

    documento, error_response = BaseViewMixin.get_object_or_404_response(Documento, pk)
    if error_response:
        return error_response

    try:
        # Usar service para interação com API externa
        zapsign_service = ZapSignService()
        
        # Deletar documento na API ZapSign
        zapsign_service.delete_document(documento.token)
        
        # Deletar documento do banco local
        documento.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    except ZapSignAPIException as e:
        logger.error(f"Erro na API ZapSign: {e.message}")
        return APIResponseHandler.error_response(
            error_message=e.message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=ERROR_CODES['ZAPSIGN_API_ERROR']
        )
    except Exception as e:
        return BaseViewMixin.handle_exception(e, "exclusão de documento")
