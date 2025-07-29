"""
Views refatoradas com padrões de projeto e DRY aplicados
"""
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
from .services import ZapSignService, DocumentoService
from .mixins import BaseViewMixin, APIResponseHandler
from .constants import HTTP_METHODS, MESSAGES
from .decorators import handle_zapsign_exceptions, validate_http_method, require_fields

import logging

logger = logging.getLogger(__name__)


@api_view([HTTP_METHODS['GET']])
@validate_http_method(HTTP_METHODS['GET'])
@handle_zapsign_exceptions("busca de documentos")
def get_documentos(request):
    """Retorna lista de todos os documentos"""
    documentos = Documento.objects.all()
    return BaseViewMixin.serialize_and_respond(
        documentos, 
        DocumentoWithSignersSerializer, 
        many=True
    )


@api_view([HTTP_METHODS['GET']])
@validate_http_method(HTTP_METHODS['GET'])
@handle_zapsign_exceptions("busca de documento")
def get_documento(request, pk):
    """Retorna um documento específico por ID"""
    documento, error_response = BaseViewMixin.get_object_or_404_response(Documento, pk)
    if error_response:
        return error_response

    return BaseViewMixin.serialize_and_respond(documento, DocumentoWithSignersSerializer)


@api_view([HTTP_METHODS['POST']])
@validate_http_method(HTTP_METHODS['POST'])
@require_fields(['name', 'url_documento', 'nome_signatario', 'email_signatario'])
@handle_zapsign_exceptions("criação de documento")
def create_documento(request):
    """Cria um novo documento"""
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


@api_view([HTTP_METHODS['PUT']])
@validate_http_method(HTTP_METHODS['PUT'])
@require_fields(['name'])
@handle_zapsign_exceptions("atualização de documento")
def update_documento(request, pk):
    """Atualiza um documento existente"""
    documento, error_response = BaseViewMixin.get_object_or_404_response(Documento, pk)
    if error_response:
        return error_response

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


@api_view([HTTP_METHODS['DELETE']])
@validate_http_method(HTTP_METHODS['DELETE'])
@handle_zapsign_exceptions("exclusão de documento")
def delete_documento(request, pk):
    """Deleta um documento existente"""
    documento, error_response = BaseViewMixin.get_object_or_404_response(Documento, pk)
    if error_response:
        return error_response

    # Usar service para interação com API externa
    zapsign_service = ZapSignService()
    
    # Deletar documento na API ZapSign
    zapsign_service.delete_document(documento.token)
    
    # Deletar documento do banco local
    documento.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
