"""
Emergency Backend - Configurações do Sistema
Centraliza todas as configurações da aplicação
"""

import os
from pathlib import Path

class Config:
    """Configurações principais do sistema"""
    
    # Chave secreta para tokens e sessões
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'emergency-backend-super-secret-key-2024'
    
    # Configurações do banco de dados
    BASE_DIR = Path(__file__).parent.parent
    DATABASE_PATH = BASE_DIR / 'database' / 'emergency_backend.db'
    
    # Configurações de segurança
    TOKEN_EXPIRATION_HOURS = 24
    PASSWORD_MIN_LENGTH = 6
    
    # Configurações do Flask
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Configurações de CORS
    CORS_ORIGINS = ["*"]
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS = ["Content-Type", "Authorization"]
    
    # Configurações de resposta da API
    DEFAULT_RESPONSE_FORMAT = {
        "status": "success",
        "mensagem": "",
        "dados": None
    }
    
    # Configurações de logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @staticmethod
    def get_database_url():
        """Retorna a URL de conexão com o banco de dados"""
        return f"sqlite:///{Config.DATABASE_PATH}"
    
    @staticmethod
    def ensure_database_directory():
        """Garante que o diretório do banco de dados existe"""
        Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        return Config.DATABASE_PATH