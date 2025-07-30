"""
Emergency Backend - Gerenciador de Sessões
Valida sessão ativa com token recebido nos headers
"""

from .token_utils import verificar_token, extrair_info_token
from database.models import Usuario
import logging

logger = logging.getLogger(__name__)

def validar_sessao(usuario_id, token):
    """
    Valida se uma sessão está ativa e válida
    
    Args:
        usuario_id (int): ID do usuário
        token (str): Token de autenticação
    
    Returns:
        bool: True se sessão válida, False caso contrário
    """
    try:
        # Verificar se o token é válido
        token_usuario_id = verificar_token(token)
        
        if not token_usuario_id:
            logger.warning(f"Token inválido na validação de sessão para usuário {usuario_id}")
            return False
        
        # Verificar se o usuario_id do token corresponde ao solicitado
        if token_usuario_id != usuario_id:
            logger.warning(f"Mismatch de usuário: token={token_usuario_id}, solicitado={usuario_id}")
            return False
        
        # Verificar se o usuário ainda existe no banco
        usuario = Usuario.buscar_por_id(usuario_id)
        if not usuario:
            logger.warning(f"Usuário {usuario_id} não encontrado durante validação de sessão")
            return False
        
        # Atualizar última atividade
        Usuario.atualizar_ultima_atividade(usuario_id)
        
        logger.info(f"Sessão validada com sucesso para usuário {usuario_id}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao validar sessão: {e}")
        return False

def obter_info_sessao(token):
    """
    Obtém informações detalhadas da sessão
    
    Args:
        token (str): Token de autenticação
    
    Returns:
        dict or None: Informações da sessão ou None se inválida
    """
    try:
        # Extrair informações do token
        info_token = extrair_info_token(token)
        
        if not info_token:
            return None
        
        usuario_id = info_token.get('usuario_id')
        
        if not usuario_id:
            return None
        
        # Buscar dados do usuário
        usuario = Usuario.buscar_por_id(usuario_id)
        
        if not usuario:
            return None
        
        # Compilar informações da sessão
        info_sessao = {
            'usuario': {
                'id': usuario['id'],
                'nome': usuario['nome'],
                'email': usuario['email'],
                'ultima_atividade': usuario['ultima_atividade']
            },
            'token': {
                'timestamp': info_token.get('timestamp'),
                'expiracao': info_token.get('expiracao'),
                'timestamp_legivel': info_token.get('timestamp_legivel'),
                'expiracao_legivel': info_token.get('expiracao_legivel'),
                'tempo_restante_segundos': info_token.get('tempo_restante_segundos'),
                'temporario': info_token.get('temporario', False)
            }
        }
        
        return info_sessao
        
    except Exception as e:
        logger.error(f"Erro ao obter informações da sessão: {e}")
        return None

def invalidar_sessao(usuario_id):
    """
    Invalida uma sessão (para logout)
    
    Nota: Como usamos tokens stateless, esta função apenas registra o logout
    O token continuará válido até expirar naturalmente
    
    Args:
        usuario_id (int): ID do usuário
    
    Returns:
        bool: True se logout registrado com sucesso
    """
    try:
        # Atualizar última atividade
        Usuario.atualizar_ultima_atividade(usuario_id)
        
        logger.info(f"Logout registrado para usuário {usuario_id}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao invalidar sessão: {e}")
        return False

def sessao_ativa(token):
    """
    Verifica se existe uma sessão ativa para o token
    
    Args:
        token (str): Token de autenticação
    
    Returns:
        bool: True se sessão ativa
    """
    try:
        usuario_id = verificar_token(token)
        
        if not usuario_id:
            return False
        
        return validar_sessao(usuario_id, token)
        
    except Exception as e:
        logger.error(f"Erro ao verificar sessão ativa: {e}")
        return False

def obter_usuario_da_sessao(token):
    """
    Obtém dados do usuário a partir do token de sessão
    
    Args:
        token (str): Token de autenticação
    
    Returns:
        dict or None: Dados do usuário ou None se inválido
    """
    try:
        usuario_id = verificar_token(token)
        
        if not usuario_id:
            return None
        
        if not validar_sessao(usuario_id, token):
            return None
        
        return Usuario.buscar_por_id(usuario_id)
        
    except Exception as e:
        logger.error(f"Erro ao obter usuário da sessão: {e}")
        return None