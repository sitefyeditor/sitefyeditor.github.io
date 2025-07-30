"""
Emergency Backend - Utilitários de Token
Gera tokens baseados no ID do usuário com timestamp e verificação
Usa hashlib e time para tokens temporários
"""

import hashlib
import time
import json
import base64
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

def gerar_token(usuario_id):
    """
    Gera um token de autenticação baseado no ID do usuário
    
    Args:
        usuario_id (int): ID do usuário
    
    Returns:
        str: Token de autenticação codificado
    """
    try:
        # Timestamp atual
        timestamp = int(time.time())
        
        # Timestamp de expiração (24 horas)
        expiracao = timestamp + (Config.TOKEN_EXPIRATION_HOURS * 3600)
        
        # Dados do token
        token_data = {
            'usuario_id': usuario_id,
            'timestamp': timestamp,
            'expiracao': expiracao
        }
        
        # Converter para JSON
        json_data = json.dumps(token_data, sort_keys=True)
        
        # Gerar hash de verificação
        hash_verificacao = hashlib.sha256(
            (json_data + Config.SECRET_KEY).encode('utf-8')
        ).hexdigest()
        
        # Dados finais do token
        token_final = {
            'data': token_data,
            'hash': hash_verificacao
        }
        
        # Codificar em base64
        token_json = json.dumps(token_final)
        token_base64 = base64.b64encode(token_json.encode('utf-8')).decode('utf-8')
        
        logger.info(f"Token gerado para usuário {usuario_id}, expira em {expiracao}")
        return token_base64
        
    except Exception as e:
        logger.error(f"Erro ao gerar token: {e}")
        return None

def verificar_token(token):
    """
    Verifica se um token é válido e não expirou
    
    Args:
        token (str): Token a ser verificado
    
    Returns:
        int or None: ID do usuário se válido, None caso contrário
    """
    try:
        # Decodificar base64
        token_json = base64.b64decode(token.encode('utf-8')).decode('utf-8')
        token_data = json.loads(token_json)
        
        # Extrair dados
        data = token_data.get('data', {})
        hash_recebido = token_data.get('hash', '')
        
        usuario_id = data.get('usuario_id')
        timestamp = data.get('timestamp')
        expiracao = data.get('expiracao')
        
        if not all([usuario_id, timestamp, expiracao]):
            logger.warning("Token com dados incompletos")
            return None
        
        # Verificar expiração
        timestamp_atual = int(time.time())
        if timestamp_atual > expiracao:
            logger.warning(f"Token expirado para usuário {usuario_id}")
            return None
        
        # Verificar hash
        json_data = json.dumps(data, sort_keys=True)
        hash_esperado = hashlib.sha256(
            (json_data + Config.SECRET_KEY).encode('utf-8')
        ).hexdigest()
        
        if hash_recebido != hash_esperado:
            logger.warning(f"Token com hash inválido para usuário {usuario_id}")
            return None
        
        logger.info(f"Token válido verificado para usuário {usuario_id}")
        return usuario_id
        
    except Exception as e:
        logger.error(f"Erro ao verificar token: {e}")
        return None

def extrair_info_token(token):
    """
    Extrai informações de um token sem verificar validade
    Útil para debug e logs
    
    Args:
        token (str): Token para extrair informações
    
    Returns:
        dict or None: Informações do token ou None se erro
    """
    try:
        # Decodificar base64
        token_json = base64.b64decode(token.encode('utf-8')).decode('utf-8')
        token_data = json.loads(token_json)
        
        data = token_data.get('data', {})
        
        # Converter timestamps para formato legível
        if 'timestamp' in data:
            data['timestamp_legivel'] = time.ctime(data['timestamp'])
        
        if 'expiracao' in data:
            data['expiracao_legivel'] = time.ctime(data['expiracao'])
            data['tempo_restante_segundos'] = data['expiracao'] - int(time.time())
        
        return data
        
    except Exception as e:
        logger.error(f"Erro ao extrair informações do token: {e}")
        return None

def token_expirado(token):
    """
    Verifica se um token está expirado (sem verificar hash)
    
    Args:
        token (str): Token para verificar
    
    Returns:
        bool: True se expirado, False caso contrário
    """
    try:
        info = extrair_info_token(token)
        
        if not info or 'expiracao' not in info:
            return True
        
        timestamp_atual = int(time.time())
        return timestamp_atual > info['expiracao']
        
    except Exception as e:
        logger.error(f"Erro ao verificar expiração do token: {e}")
        return True

def renovar_token(token):
    """
    Renova um token válido por mais 24 horas
    
    Args:
        token (str): Token atual
    
    Returns:
        str or None: Novo token ou None se inválido
    """
    try:
        usuario_id = verificar_token(token)
        
        if not usuario_id:
            return None
        
        # Gerar novo token
        return gerar_token(usuario_id)
        
    except Exception as e:
        logger.error(f"Erro ao renovar token: {e}")
        return None

def gerar_token_temporario(usuario_id, duracao_minutos=60):
    """
    Gera um token com duração customizada
    
    Args:
        usuario_id (int): ID do usuário
        duracao_minutos (int): Duração em minutos
    
    Returns:
        str: Token temporário
    """
    try:
        timestamp = int(time.time())
        expiracao = timestamp + (duracao_minutos * 60)
        
        token_data = {
            'usuario_id': usuario_id,
            'timestamp': timestamp,
            'expiracao': expiracao,
            'temporario': True
        }
        
        json_data = json.dumps(token_data, sort_keys=True)
        hash_verificacao = hashlib.sha256(
            (json_data + Config.SECRET_KEY).encode('utf-8')
        ).hexdigest()
        
        token_final = {
            'data': token_data,
            'hash': hash_verificacao
        }
        
        token_json = json.dumps(token_final)
        token_base64 = base64.b64encode(token_json.encode('utf-8')).decode('utf-8')
        
        logger.info(f"Token temporário gerado para usuário {usuario_id}, duração: {duracao_minutos}min")
        return token_base64
        
    except Exception as e:
        logger.error(f"Erro ao gerar token temporário: {e}")
        return None