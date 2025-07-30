"""
Emergency Backend - Rotas HTTP
Define todas as rotas públicas e protegidas da API
"""

from flask import Blueprint, request, jsonify
from .auth import token_required
from core.interpreter import processar_comando
from core.actions import *
import logging

logger = logging.getLogger(__name__)

def create_routes_blueprint():
    """Cria blueprint com todas as rotas da aplicação"""
    routes_bp = Blueprint('routes', __name__)
    
    def create_response(status="success", mensagem="", dados=None):
        """Cria resposta padronizada da API"""
        return jsonify({
            "status": status,
            "mensagem": mensagem,
            "dados": dados
        })
    
    @routes_bp.route('/salvar_projeto', methods=['POST'])
    @token_required
    def salvar_projeto_route(usuario_id):
        """
        Rota para salvar um projeto HTML
        Requer autenticação via token
        """
        try:
            data = request.get_json()
            
            if not data:
                return create_response("error", "Dados JSON não fornecidos"), 400
            
            titulo = data.get('titulo')
            conteudo_html = data.get('conteudo_html')
            projeto_id = data.get('projeto_id')  # Para atualizações
            
            if not titulo:
                return create_response("error", "Título é obrigatório"), 400
            
            if not conteudo_html:
                return create_response("error", "Conteúdo HTML é obrigatório"), 400
            
            # Salvar projeto
            resultado = salvar_projeto(usuario_id, titulo, conteudo_html, projeto_id)
            
            if resultado:
                return create_response(
                    "success",
                    "Projeto salvo com sucesso",
                    resultado
                )
            else:
                return create_response("error", "Erro ao salvar projeto"), 500
                
        except Exception as e:
            logger.error(f"Erro na rota salvar_projeto: {e}")
            return create_response("error", "Erro interno do servidor"), 500
    
    @routes_bp.route('/carregar_projeto/<int:projeto_id>', methods=['GET'])
    @token_required
    def carregar_projeto_route(usuario_id, projeto_id):
        """
        Rota para carregar um projeto específico
        Requer autenticação via token
        """
        try:
            resultado = carregar_projeto(usuario_id, projeto_id)
            
            if resultado:
                return create_response(
                    "success",
                    "Projeto carregado com sucesso",
                    resultado
                )
            else:
                return create_response("error", "Projeto não encontrado"), 404
                
        except Exception as e:
            logger.error(f"Erro na rota carregar_projeto: {e}")
            return create_response("error", "Erro interno do servidor"), 500
    
    @routes_bp.route('/listar_projetos', methods=['GET'])
    @token_required
    def listar_projetos_route(usuario_id):
        """
        Rota para listar todos os projetos do usuário
        Requer autenticação via token
        """
        try:
            projetos = listar_projetos(usuario_id)
            
            return create_response(
                "success",
                f"Encontrados {len(projetos)} projetos",
                projetos
            )
            
        except Exception as e:
            logger.error(f"Erro na rota listar_projetos: {e}")
            return create_response("error", "Erro interno do servidor"), 500
    
    @routes_bp.route('/deletar_projeto/<int:projeto_id>', methods=['DELETE'])
    @token_required
    def deletar_projeto_route(usuario_id, projeto_id):
        """
        Rota para deletar um projeto
        Requer autenticação via token
        """
        try:
            sucesso = deletar_projeto(usuario_id, projeto_id)
            
            if sucesso:
                return create_response(
                    "success",
                    "Projeto deletado com sucesso"
                )
            else:
                return create_response("error", "Projeto não encontrado ou não autorizado"), 404
                
        except Exception as e:
            logger.error(f"Erro na rota deletar_projeto: {e}")
            return create_response("error", "Erro interno do servidor"), 500
    
    @routes_bp.route('/comando', methods=['POST'])
    @token_required
    def comando_route(usuario_id):
        """
        Rota para processar comandos via JSON
        Recebe JSON com campo 'acao' e redireciona para função apropriada
        """
        try:
            data = request.get_json()
            
            if not data:
                return create_response("error", "Dados JSON não fornecidos"), 400
            
            acao = data.get('acao')
            
            if not acao:
                return create_response("error", "Campo 'acao' é obrigatório"), 400
            
            # Processar comando através do interpreter
            resultado = processar_comando(usuario_id, acao, data)
            
            if resultado.get('status') == 'success':
                return create_response(
                    "success",
                    resultado.get('mensagem', 'Comando executado com sucesso'),
                    resultado.get('dados')
                )
            else:
                return create_response(
                    "error",
                    resultado.get('mensagem', 'Erro ao executar comando')
                ), 400
                
        except Exception as e:
            logger.error(f"Erro na rota comando: {e}")
            return create_response("error", "Erro interno do servidor"), 500
    
    @routes_bp.route('/status', methods=['GET'])
    def status_route():
        """Rota pública para verificar status do servidor"""
        from database.db import get_database_info
        
        try:
            db_info = get_database_info()
            
            return create_response(
                "success",
                "Emergency Backend funcionando normalmente",
                {
                    "servidor": "online",
                    "database": db_info,
                    "version": "1.0.0"
                }
            )
            
        except Exception as e:
            logger.error(f"Erro na rota status: {e}")
            return create_response("error", "Erro ao verificar status"), 500
    
    return routes_bp