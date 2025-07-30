#!/usr/bin/env python3
"""
Emergency Backend - Servidor Flask Principal
Sistema completo de gerenciamento de projetos HTML com autenticação
"""

from flask import Flask
from flask_cors import CORS
from api import create_api_blueprint
from database.db import init_database
from config.settings import Config
import logging
import os

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config.from_object(Config)
    
    # CORS para permitir requisições do frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Inicializar banco de dados
    init_database()
    
    # Registrar blueprints
    api_blueprint = create_api_blueprint()
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    @app.route('/')
    def root():
        return {
            "status": "success",
            "mensagem": "Emergency Backend API está funcionando!",
            "version": "1.0.0",
            "endpoints": [
                "/api/cadastro",
                "/api/login", 
                "/api/salvar_projeto",
                "/api/carregar_projeto",
                "/api/listar_projetos",
                "/api/deletar_projeto",
                "/api/comando"
            ]
        }
    
    @app.route('/health')
    def health_check():
        return {
            "status": "success",
            "mensagem": "Servidor funcionando normalmente",
            "database": "conectado"
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Configurações do servidor
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 8001))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    EMERGENCY BACKEND                         ║
║                                                              ║
║  🚀 Servidor iniciado com sucesso!                          ║
║  📡 Host: {host}                                    ║
║  🔌 Porta: {port}                                           ║
║  🔧 Debug: {debug_mode}                                      ║
║  💾 Database: SQLite                                         ║
║                                                              ║
║  📚 Rotas disponíveis:                                      ║
║    • POST /api/cadastro - Cadastrar usuário                 ║
║    • POST /api/login - Fazer login                          ║
║    • POST /api/salvar_projeto - Salvar projeto HTML         ║
║    • GET  /api/carregar_projeto/<id> - Carregar projeto     ║
║    • GET  /api/listar_projetos - Listar projetos do usuário ║
║    • DELETE /api/deletar_projeto/<id> - Deletar projeto     ║
║    • POST /api/comando - Executar comandos via JSON         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        threaded=True
    )