"""
Emergency Backend - API Package
Centraliza todas as rotas HTTP da aplicação
"""

from flask import Blueprint
from .routes import create_routes_blueprint
from .auth import create_auth_blueprint

def create_api_blueprint():
    """
    Cria e configura o blueprint principal da API
    Registra todas as rotas da aplicação
    """
    # Criar blueprint principal da API
    api_bp = Blueprint('api', __name__)
    
    # Registrar sub-blueprints
    routes_bp = create_routes_blueprint()
    auth_bp = create_auth_blueprint()
    
    # Registrar blueprints no blueprint principal
    api_bp.register_blueprint(routes_bp)
    api_bp.register_blueprint(auth_bp)
    
    return api_bp