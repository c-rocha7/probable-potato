"""
Configurações da aplicação
"""
from decouple import config

class AppConfig:
    """Classe para centralizar configurações da aplicação"""
    
    # Configurações da API ZapSign
    ZAPSIGN_API_TOKEN = config('ZAPSIGN_API_TOKEN')
    ZAPSIGN_API_BASE_URL = config('ZAPSIGN_API_BASE_URL')
    
    # Configurações de logging
    LOG_LEVEL = config('LOG_LEVEL', default='INFO')
    
    # Configurações de timeout
    REQUEST_TIMEOUT = config('REQUEST_TIMEOUT', default=30, cast=int)
    
    @classmethod
    def get_zapsign_config(cls):
        """Retorna configurações específicas do ZapSign"""
        return {
            'token': cls.ZAPSIGN_API_TOKEN,
            'base_url': cls.ZAPSIGN_API_BASE_URL,
            'timeout': cls.REQUEST_TIMEOUT
        }
