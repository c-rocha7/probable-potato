"""
Constantes da aplicação
"""

# Status de documentos
DOCUMENT_STATUS = {
    'PENDING': 'pending',
    'SIGNED': 'signed',
    'CANCELLED': 'cancelled',
    'EXPIRED': 'expired'
}

# Status de signatários
SIGNER_STATUS = {
    'PENDING': 'pending',
    'SIGNED': 'signed',
    'DECLINED': 'declined'
}

# Métodos HTTP permitidos
HTTP_METHODS = {
    'GET': 'GET',
    'POST': 'POST',
    'PUT': 'PUT',
    'DELETE': 'DELETE',
    'PATCH': 'PATCH'
}

# Códigos de erro customizados
ERROR_CODES = {
    'ZAPSIGN_API_ERROR': 'ZAPSIGN_001',
    'DOCUMENT_NOT_FOUND': 'DOC_001',
    'SIGNER_NOT_FOUND': 'SIGN_001',
    'VALIDATION_ERROR': 'VAL_001',
    'EXTERNAL_API_ERROR': 'EXT_001'
}

# Mensagens padrão
MESSAGES = {
    'DOCUMENT_CREATED': 'Documento criado com sucesso',
    'DOCUMENT_UPDATED': 'Documento atualizado com sucesso',
    'DOCUMENT_DELETED': 'Documento deletado com sucesso',
    'SIGNER_ADDED': 'Signatário adicionado com sucesso',
    'OPERATION_SUCCESS': 'Operação realizada com sucesso'
}

# Configurações padrão
DEFAULT_VALUES = {
    'COMPANY_ID': 1,
    'EXTERNAL_ID': 'vazio',
    'CREATED_BY': 'system'
}
