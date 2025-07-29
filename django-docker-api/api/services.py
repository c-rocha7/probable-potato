import requests
from typing import Dict, Any, Optional
from rest_framework import status
from rest_framework.response import Response
from .config import AppConfig
from .constants import DEFAULT_VALUES


class ZapSignAPIException(Exception):
    """Exceção customizada para erros da API ZapSign"""
    def __init__(self, message: str, status_code: int = None, response_data: Dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class ZapSignService:
    """Service para interações com a API ZapSign"""
    
    def __init__(self):
        config_data = AppConfig.get_zapsign_config()
        self.api_token = config_data['token']
        self.base_url = config_data['base_url']
        self.timeout = config_data['timeout']
        self.headers = self._get_headers()
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna os headers necessários para autenticação na API ZapSign"""
        return {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Processa a resposta da API e levanta exceção se necessário"""
        if response.status_code != 200:
            raise ZapSignAPIException(
                message=f"Erro na API ZapSign: {response.text}",
                status_code=response.status_code,
                response_data=response.json() if response.content else None
            )
        return response.json()
    
    def create_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um documento na API ZapSign"""
        payload = {
            "name": document_data.get("name"),
            "url_pdf": document_data.get("url_documento"),
            "signers": [
                {
                    "name": document_data.get("nome_signatario"),
                    "email": document_data.get("email_signatario"),
                }
            ],
        }
        
        response = requests.post(
            f'{self.base_url}/docs/',
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        
        return self._handle_response(response)
    
    def update_document(self, token: str, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um documento na API ZapSign"""
        payload = {
            "name": document_data.get("name"),
        }
        
        response = requests.put(
            f'{self.base_url}/docs/{token}/',
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        
        return self._handle_response(response)
    
    def delete_document(self, token: str) -> None:
        """Deleta um documento na API ZapSign"""
        response = requests.delete(
            f'{self.base_url}/docs/{token}/',
            headers=self.headers,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            raise ZapSignAPIException(
                message=f"Erro ao deletar documento: {response.text}",
                status_code=response.status_code
            )
    
    def add_signer(self, document_token: str, signer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona um signatário a um documento"""
        payload = {
            "name": signer_data.get("name"),
            "email": signer_data.get("email"),
        }
        
        response = requests.post(
            f'{self.base_url}/docs/{document_token}/add-signer/',
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        
        return self._handle_response(response)


class DocumentoService:
    """Service para operações com documentos"""
    
    def __init__(self):
        self.zapsign_service = ZapSignService()
    
    def prepare_document_data(self, api_result: Dict[str, Any], request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepara os dados do documento para salvamento no banco"""
        return {
            **request_data,
            'openID': api_result.get('open_id'),
            'token': api_result.get('token'),
            'status': api_result.get('status', 'pending'),
            'created_by': api_result.get('created_by', {}).get('email', DEFAULT_VALUES['CREATED_BY']),
            'company_id': request_data.get('company_id', DEFAULT_VALUES['COMPANY_ID']),
            'external_id': api_result.get('external_id', DEFAULT_VALUES['EXTERNAL_ID'])
        }
    
    def prepare_signer_data(self, api_result: Dict[str, Any], request_data: Dict[str, Any], document_id: int) -> Dict[str, Any]:
        """Prepara os dados do signatário para salvamento no banco"""
        return {
            'token': api_result.get('token'),
            'status': api_result.get('status', 'pending'),
            'name': request_data.get("nome_signatario"),
            'email': request_data.get("email_signatario"),
            'external_id': api_result.get('external_id', DEFAULT_VALUES['EXTERNAL_ID']),
            'documentID': document_id
        }
