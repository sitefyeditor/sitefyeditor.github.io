"""
Emergency Backend - Sistema de Autenticação
Gerencia autenticação completa: cadastro, login, tokens e verificação de sessão
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from database.models import Usuario
from utils.token_utils import gerar_token, verificar_token
from utils.session import validar_sessao
import logging

logger = logging.getLogger(__name__)

def create_auth_blueprint():
    """Cria blueprint com rotas de autenticação"""
    auth_bp = Blueprint('auth', __name__)
    
    def create_response(status="success", mensagem="", dados=None):
        """Cria resposta padronizada da API"""
        return jsonify({
            "status": status,
            "mensagem": mensagem,
            "dados": dados
        })
    
    @auth_bp.route('/cadastro', methods=['POST'])
    def cadastro():
        """
        Rota para cadastro de novos usuários
        Criptografa senha usando werkzeug.security
        """
        try:
            data = request.get_json()
            
            if not data:
                return create_response("error", "Dados JSON não fornecidos"), 400
            
            nome = data.get('nome', '').strip()
            email = data.get('email', '').strip().lower()
            senha = data.get('senha', '')
            
            # Validações
            if not nome:
                return create_response("error", "Nome é obrigatório"), 400
            
            if not email:
                return create_response("error", "Email é obrigatório"), 400
            
            if not senha:
                return create_response("error", "Senha é obrigatória"), 400
            
            if len(senha) < 6:
                return create_response("error", "Senha deve ter pelo menos 6 caracteres"), 400
            
            if '@' not in email:
                return create_response("error", "Email inválido"), 400
            
            # Verificar se usuário já existe
            usuario_existente = Usuario.buscar_por_email(email)
            if usuario_existente:
                return create_response("error", "Email já está em uso"), 409
            
            # Criar usuário
            usuario = Usuario.criar_usuario(nome, email, senha)
            
            if usuario:
                # Gerar token de autenticação
                token = gerar_token(usuario['id'])
                
                return create_response(
                    "success",
                    "Usuário cadastrado com sucesso",
                    {
                        "usuario": {
                            "id": usuario['id'],
                            "nome": usuario['nome'],
                            "email": usuario['email']
                        },
                        "token": token
                    }
                )
            else:
                return create_response("error", "Erro ao criar usuário"), 500
                
        except Exception as e:
            logger.error(f"Erro no cadastro: {e}")
            return create_response("error", "Erro interno do servidor"), 500
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        """
        Rota para login de usuários
        Verifica hash da senha e gera token de autenticação
        """
        try:
            data = request.get_json()
            
            if not data:
                return create_response("error", "Dados JSON não fornecidos"), 400
            
            email = data.get('email', '').strip().lower()
            senha = data.get('senha', '')
            
            # Validações
            if not email:
                return create_response("error", "Email é obrigatório"), 400
            
            if not senha:
                return create_response("error", "Senha é obrigatória"), 400
            
            # Verificar credenciais
            usuario = Usuario.verificar_senha(email, senha)
            
            if usuario:
                # Gerar token de autenticação
                token = gerar_token(usuario['id'])
                
                return create_response(
                    "success",
                    "Login realizado com sucesso", 
                    {
                        "usuario": {
                            "id": usuario['id'],
                            "nome": usuario['nome'],
                            "email": usuario['email']
                        },
                        "token": token
                    }
                )
            else:
                return create_response("error", "Email ou senha incorretos"), 401
                
        except Exception as e:
            logger.error(f"Erro no login: {e}")
            return create_response("error", "Erro interno do servidor"), 500
    
    return auth_bp

def token_required(f):
    """
    Decorator para proteger rotas que exigem autenticação
    Verifica token enviado no header Authorization
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Buscar token no header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Formato esperado: "Bearer TOKEN"
                token = auth_header.split(" ")[1] if auth_header.startswith('Bearer ') else auth_header
            except IndexError:
                pass
        
        if not token:
            return jsonify({
                "status": "error", 
                "mensagem": "Token de autenticação não fornecido"
            }), 401
        
        try:
            # Verificar token
            usuario_id = verificar_token(token)
            
            if not usuario_id:
                return jsonify({
                    "status": "error",
                    "mensagem": "Token inválido ou expirado"
                }), 401
            
            # Validar sessão
            if not validar_sessao(usuario_id, token):
                return jsonify({
                    "status": "error",
                    "mensagem": "Sessão inválida"
                }), 401
            
            # Chamar função original passando usuario_id
            return f(usuario_id, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Erro na verificação do token: {e}")
            return jsonify({
                "status": "error",
                "mensagem": "Erro na autenticação"
            }), 401
    
    return decorated