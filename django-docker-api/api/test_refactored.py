"""
Testes para as views refatoradas
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, Mock
from .models import Documento, Signatario, Empresa
from .services import ZapSignService, ZapSignAPIException


class DocumentoViewsTest(APITestCase):
    """Testes para as views de documentos"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.empresa = Empresa.objects.create(
            name="Empresa Teste",
            apiToken="token_teste"
        )
        
        self.documento = Documento.objects.create(
            openID=123,
            token="token_doc_teste",
            name="Documento Teste",
            status="pending",
            created_by="test@test.com",
            company_id=self.empresa,
            externalID="ext_123"
        )
    
    def test_get_documentos_success(self):
        """Testa a listagem de documentos com sucesso"""
        url = reverse('get_documentos')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
    
    def test_get_documento_success(self):
        """Testa a busca de um documento específico com sucesso"""
        url = reverse('get_documento', kwargs={'pk': self.documento.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.documento.name)
    
    def test_get_documento_not_found(self):
        """Testa a busca de um documento inexistente"""
        url = reverse('get_documento', kwargs={'pk': 99999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @patch('api.services.ZapSignService.create_document')
    def test_create_documento_success(self, mock_create_document):
        """Testa a criação de documento com sucesso"""
        mock_create_document.return_value = {
            'open_id': 456,
            'token': 'new_token',
            'status': 'pending',
            'created_by': {'email': 'test@test.com'},
            'external_id': 'ext_456'
        }
        
        url = reverse('create_documento')
        data = {
            'name': 'Novo Documento',
            'url_documento': 'http://example.com/doc.pdf',
            'nome_signatario': 'João Silva',
            'email_signatario': 'joao@test.com',
            'company_id': self.empresa.id
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_create_document.assert_called_once_with(data)
    
    @patch('api.services.ZapSignService.create_document')
    def test_create_documento_missing_field(self, mock_create_document):
        """Testa a criação de documento com campo obrigatório ausente"""
        url = reverse('create_documento')
        data = {
            'name': 'Novo Documento',
            # faltando campos obrigatórios
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_create_document.assert_not_called()
    
    @patch('api.services.ZapSignService.update_document')
    def test_update_documento_success(self, mock_update_document):
        """Testa a atualização de documento com sucesso"""
        mock_update_document.return_value = {'success': True}
        
        url = reverse('update_documento', kwargs={'pk': self.documento.pk})
        data = {'name': 'Documento Atualizado'}
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_update_document.assert_called_once_with(self.documento.token, data)
    
    @patch('api.services.ZapSignService.delete_document')
    def test_delete_documento_success(self, mock_delete_document):
        """Testa a exclusão de documento com sucesso"""
        mock_delete_document.return_value = None
        
        url = reverse('delete_documento', kwargs={'pk': self.documento.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_delete_document.assert_called_once_with(self.documento.token)


class ZapSignServiceTest(TestCase):
    """Testes para o service ZapSign"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.service = ZapSignService()
    
    @patch('api.services.requests.post')
    def test_create_document_success(self, mock_post):
        """Testa a criação de documento na API ZapSign"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'open_id': 123,
            'token': 'test_token',
            'status': 'pending'
        }
        mock_post.return_value = mock_response
        
        document_data = {
            'name': 'Test Document',
            'url_documento': 'http://example.com/doc.pdf',
            'nome_signatario': 'Test User',
            'email_signatario': 'test@example.com'
        }
        
        result = self.service.create_document(document_data)
        
        self.assertEqual(result['token'], 'test_token')
        mock_post.assert_called_once()
    
    @patch('api.services.requests.post')
    def test_create_document_api_error(self, mock_post):
        """Testa erro na API ZapSign durante criação"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Bad Request'
        mock_response.content = b'{"error": "Invalid data"}'
        mock_post.return_value = mock_response
        
        document_data = {
            'name': 'Test Document',
            'url_documento': 'http://example.com/doc.pdf',
            'nome_signatario': 'Test User',
            'email_signatario': 'test@example.com'
        }
        
        with self.assertRaises(ZapSignAPIException):
            self.service.create_document(document_data)
