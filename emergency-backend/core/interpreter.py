"""
Emergency Backend - Interpretador de Comandos
Recebe comandos via JSON e redireciona para actions.py
"""

from .actions import (
    salvar_projeto, carregar_projeto, listar_projetos, 
    deletar_projeto, obter_estatisticas_usuario
)
import logging

logger = logging.getLogger(__name__)

def processar_comando(usuario_id, acao, dados):
    """
    Processa comandos JSON e redireciona para funções apropriadas
    
    Args:
        usuario_id (int): ID do usuário autenticado
        acao (str): Ação a ser executada
        dados (dict): Dados enviados com o comando
    
    Returns:
        dict: Resultado da operação com status, mensagem e dados
    """
    
    logger.info(f"Processando comando: {acao} para usuário {usuario_id}")
    
    try:
        # Mapeamento de ações para funções
        acoes_disponiveis = {
            'salvar_projeto': _processar_salvar_projeto,
            'carregar_projeto': _processar_carregar_projeto,
            'listar_projetos': _processar_listar_projetos,
            'deletar_projeto': _processar_deletar_projeto,
            'estatisticas': _processar_estatisticas,
            'status_usuario': _processar_status_usuario
        }
        
        if acao not in acoes_disponiveis:
            return {
                'status': 'error',
                'mensagem': f'Ação "{acao}" não reconhecida',
                'acoes_disponiveis': list(acoes_disponiveis.keys())
            }
        
        # Executar ação
        resultado = acoes_disponiveis[acao](usuario_id, dados)
        
        logger.info(f"Comando {acao} executado com sucesso para usuário {usuario_id}")
        return resultado
        
    except Exception as e:
        logger.error(f"Erro ao processar comando {acao}: {e}")
        return {
            'status': 'error',
            'mensagem': f'Erro interno ao processar comando: {str(e)}'
        }

def _processar_salvar_projeto(usuario_id, dados):
    """Processa comando de salvar projeto"""
    titulo = dados.get('titulo')
    conteudo_html = dados.get('conteudo_html')
    projeto_id = dados.get('projeto_id')
    
    if not titulo:
        return {
            'status': 'error',
            'mensagem': 'Título é obrigatório'
        }
    
    if not conteudo_html:
        return {
            'status': 'error',
            'mensagem': 'Conteúdo HTML é obrigatório'
        }
    
    resultado = salvar_projeto(usuario_id, titulo, conteudo_html, projeto_id)
    
    if resultado:
        return {
            'status': 'success',
            'mensagem': 'Projeto salvo com sucesso',
            'dados': resultado
        }
    else:
        return {
            'status': 'error',
            'mensagem': 'Erro ao salvar projeto'
        }

def _processar_carregar_projeto(usuario_id, dados):
    """Processa comando de carregar projeto"""
    projeto_id = dados.get('projeto_id')
    
    if not projeto_id:
        return {
            'status': 'error',
            'mensagem': 'ID do projeto é obrigatório'
        }
    
    try:
        projeto_id = int(projeto_id)
    except (ValueError, TypeError):
        return {
            'status': 'error',
            'mensagem': 'ID do projeto deve ser um número'
        }
    
    resultado = carregar_projeto(usuario_id, projeto_id)
    
    if resultado:
        return {
            'status': 'success',
            'mensagem': 'Projeto carregado com sucesso',
            'dados': resultado
        }
    else:
        return {
            'status': 'error',
            'mensagem': 'Projeto não encontrado'
        }

def _processar_listar_projetos(usuario_id, dados):
    """Processa comando de listar projetos"""
    projetos = listar_projetos(usuario_id)
    
    return {
        'status': 'success',
        'mensagem': f'Encontrados {len(projetos)} projetos',
        'dados': projetos
    }

def _processar_deletar_projeto(usuario_id, dados):
    """Processa comando de deletar projeto"""
    projeto_id = dados.get('projeto_id')
    
    if not projeto_id:
        return {
            'status': 'error',
            'mensagem': 'ID do projeto é obrigatório'
        }
    
    try:
        projeto_id = int(projeto_id)
    except (ValueError, TypeError):
        return {
            'status': 'error',
            'mensagem': 'ID do projeto deve ser um número'
        }
    
    sucesso = deletar_projeto(usuario_id, projeto_id)
    
    if sucesso:
        return {
            'status': 'success',
            'mensagem': 'Projeto deletado com sucesso'
        }
    else:
        return {
            'status': 'error',
            'mensagem': 'Projeto não encontrado ou não autorizado'
        }

def _processar_estatisticas(usuario_id, dados):
    """Processa comando de obter estatísticas"""
    stats = obter_estatisticas_usuario(usuario_id)
    
    return {
        'status': 'success',
        'mensagem': 'Estatísticas obtidas com sucesso',
        'dados': stats
    }

def _processar_status_usuario(usuario_id, dados):
    """Processa comando de status do usuário"""
    from database.models import Usuario
    
    usuario = Usuario.buscar_por_id(usuario_id)
    
    if usuario:
        return {
            'status': 'success',
            'mensagem': 'Status do usuário obtido com sucesso',
            'dados': {
                'id': usuario['id'],
                'nome': usuario['nome'],
                'email': usuario['email'],
                'data_criacao': usuario['data_criacao'],
                'ultima_atividade': usuario['ultima_atividade']
            }
        }
    else:
        return {
            'status': 'error',
            'mensagem': 'Usuário não encontrado'
        }

def obter_acoes_disponiveis():
    """
    Retorna lista de ações disponíveis no interpreter
    
    Returns:
        list: Lista de ações disponíveis
    """
    return [
        'salvar_projeto',
        'carregar_projeto', 
        'listar_projetos',
        'deletar_projeto',
        'estatisticas',
        'status_usuario'
    ]