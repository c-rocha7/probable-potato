"""
Exemplo de uso das views refatoradas
"""

# Para usar as views refatoradas, você pode:

# 1. Importar diretamente das views refatoradas:
from api.views_refactored import get_documentos, create_documento

# 2. Ou substituir as imports no urls.py:
from django.urls import path
from api import views_refactored as views  # Use as views refatoradas

urlpatterns = [
    path('documentos/', views.get_documentos, name='get_documentos'),
    path('documentos/<int:pk>/', views.get_documento, name='get_documento'),  
    path('documentos/create/', views.create_documento, name='create_documento'),
    path('documentos/update/<int:pk>/', views.update_documento, name='update_documento'),
    path('documentos/delete/<int:pk>/', views.delete_documento, name='delete_documento'),
]

# 3. Para usar apenas o service layer (recomendado para lógica de negócio complexa):
from api.services import ZapSignService, DocumentoService, ZapSignAPIException

def my_custom_logic():
    zapsign_service = ZapSignService()
    documento_service = DocumentoService()
    
    # Exemplo de uso
    document_data = {
        'name': 'Meu Documento',
        'url_documento': 'https://example.com/doc.pdf',
        'nome_signatario': 'João Silva',
        'email_signatario': 'joao@example.com'
    }
    
    try:
        api_result = zapsign_service.create_document(document_data)
        prepared_data = documento_service.prepare_document_data(api_result, document_data)
        # ... continuar com a lógica
    except ZapSignAPIException as e:
        print(f"Erro na API: {e.message}")

# 4. Para usar os mixins em outras views:
from api.mixins import BaseViewMixin, APIResponseHandler
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def my_custom_view(request):
    # Validar método
    method_error = BaseViewMixin.validate_method(request, 'GET')
    if method_error:
        return method_error
    
    try:
        # Sua lógica aqui
        data = {"message": "Success"}
        return APIResponseHandler.success_response(data)
    except Exception as e:
        return BaseViewMixin.handle_exception(e, "minha operação customizada")

# 5. Para criar novos decorators:
from api.decorators import handle_zapsign_exceptions, validate_http_method, require_fields

@api_view(['POST'])
@validate_http_method('POST')
@require_fields(['campo_obrigatorio'])
@handle_zapsign_exceptions("minha operação")
def my_decorated_view(request):
    # Sua lógica aqui - decorators cuidam das validações
    return APIResponseHandler.success_response({"status": "ok"})
