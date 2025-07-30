"""
Emergency Backend - Ações do Sistema
Funções diretas para operações com projetos e usuários
Todas as funções exigem autenticação
"""

from database.models import Usuario, Projeto
import logging

logger = logging.getLogger(__name__)

def salvar_projeto(usuario_id, titulo, conteudo_html, projeto_id=None):
    """
    Salva ou atualiza um projeto HTML no banco de dados
    
    Args:
        usuario_id (int): ID do usuário proprietário
        titulo (str): Título do projeto
        conteudo_html (str): Conteúdo HTML completo
        projeto_id (int, opcional): ID para atualização (None para novo)
    
    Returns:
        dict: Dados do projeto salvo ou None se erro
    """
    try:
        logger.info(f"Salvando projeto '{titulo}' para usuário {usuario_id}")
        
        if projeto_id:
            # Atualizar projeto existente
            projeto = Projeto.atualizar_projeto(projeto_id, titulo, conteudo_html)
            if projeto:
                logger.info(f"Projeto {projeto_id} atualizado com sucesso")
            else:
                logger.warning(f"Projeto {projeto_id} não encontrado para atualização")
        else:
            # Criar novo projeto
            projeto = Projeto.criar_projeto(usuario_id, titulo, conteudo_html)
            if projeto:
                logger.info(f"Novo projeto criado com ID {projeto['id']}")
        
        return projeto
        
    except Exception as e:
        logger.error(f"Erro ao salvar projeto: {e}")
        return None

def carregar_projeto(usuario_id, projeto_id):
    """
    Carrega um projeto específico do usuário
    
    Args:
        usuario_id (int): ID do usuário
        projeto_id (int): ID do projeto
    
    Returns:
        dict: Dados do projeto ou None se não encontrado
    """
    try:
        logger.info(f"Carregando projeto {projeto_id} para usuário {usuario_id}")
        
        # Buscar projeto
        projeto = Projeto.buscar_por_id(projeto_id)
        
        if not projeto:
            logger.warning(f"Projeto {projeto_id} não encontrado")
            return None
        
        # Verificar se o projeto pertence ao usuário
        if projeto['usuario_id'] != usuario_id:
            logger.warning(f"Usuário {usuario_id} tentou acessar projeto {projeto_id} de outro usuário")
            return None
        
        logger.info(f"Projeto {projeto_id} carregado com sucesso")
        return projeto
        
    except Exception as e:
        logger.error(f"Erro ao carregar projeto: {e}")
        return None

def listar_projetos(usuario_id):
    """
    Lista todos os projetos de um usuário
    
    Args:
        usuario_id (int): ID do usuário
    
    Returns:
        list: Lista de projetos (sem conteúdo HTML completo)
    """
    try:
        logger.info(f"Listando projetos do usuário {usuario_id}")
        
        projetos = Projeto.listar_por_usuario(usuario_id)
        
        logger.info(f"Encontrados {len(projetos)} projetos para usuário {usuario_id}")
        return projetos
        
    except Exception as e:
        logger.error(f"Erro ao listar projetos: {e}")
        return []

def deletar_projeto(usuario_id, projeto_id):
    """
    Deleta um projeto do usuário
    
    Args:
        usuario_id (int): ID do usuário
        projeto_id (int): ID do projeto
    
    Returns:
        bool: True se deletado, False caso contrário
    """
    try:
        logger.info(f"Deletando projeto {projeto_id} do usuário {usuario_id}")
        
        sucesso = Projeto.deletar_projeto(projeto_id, usuario_id)
        
        if sucesso:
            logger.info(f"Projeto {projeto_id} deletado com sucesso")
        else:
            logger.warning(f"Falha ao deletar projeto {projeto_id}")
        
        return sucesso
        
    except Exception as e:
        logger.error(f"Erro ao deletar projeto: {e}")
        return False

def obter_estatisticas_usuario(usuario_id):
    """
    Obtém estatísticas do usuário e seus projetos
    
    Args:
        usuario_id (int): ID do usuário
    
    Returns:
        dict: Estatísticas do usuário
    """
    try:
        logger.info(f"Obtendo estatísticas do usuário {usuario_id}")
        
        # Buscar dados do usuário
        usuario = Usuario.buscar_por_id(usuario_id)
        if not usuario:
            return None
        
        # Contar projetos
        total_projetos = Projeto.contar_projetos_usuario(usuario_id)
        
        # Buscar projetos para estatísticas
        projetos = Projeto.listar_por_usuario(usuario_id)
        
        # Calcular estatísticas
        tamanho_total_html = sum(p.get('tamanho_html', 0) for p in projetos)
        
        # Projeto mais recente
        projeto_mais_recente = projetos[0] if projetos else None
        
        estatisticas = {
            'usuario': {
                'id': usuario['id'],
                'nome': usuario['nome'],
                'email': usuario['email'],
                'data_criacao': usuario['data_criacao'],
                'ultima_atividade': usuario['ultima_atividade']
            },
            'projetos': {
                'total': total_projetos,
                'tamanho_total_html_bytes': tamanho_total_html,
                'tamanho_total_html_kb': round(tamanho_total_html / 1024, 2),
                'projeto_mais_recente': projeto_mais_recente
            }
        }
        
        logger.info(f"Estatísticas obtidas para usuário {usuario_id}: {total_projetos} projetos")
        return estatisticas
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        return None

def verificar_projeto_pertence_usuario(usuario_id, projeto_id):
    """
    Verifica se um projeto pertence a um usuário específico
    
    Args:
        usuario_id (int): ID do usuário
        projeto_id (int): ID do projeto
    
    Returns:
        bool: True se o projeto pertence ao usuário
    """
    try:
        projeto = Projeto.buscar_por_id(projeto_id)
        
        if not projeto:
            return False
        
        return projeto['usuario_id'] == usuario_id
        
    except Exception as e:
        logger.error(f"Erro ao verificar propriedade do projeto: {e}")
        return False

def obter_preview_projeto(usuario_id, projeto_id, max_chars=500):
    """
    Obtém um preview do conteúdo HTML de um projeto
    
    Args:
        usuario_id (int): ID do usuário
        projeto_id (int): ID do projeto
        max_chars (int): Máximo de caracteres do preview
    
    Returns:
        dict: Preview do projeto ou None se erro
    """
    try:
        projeto = carregar_projeto(usuario_id, projeto_id)
        
        if not projeto:
            return None
        
        conteudo_html = projeto['conteudo_html']
        preview = conteudo_html[:max_chars]
        
        if len(conteudo_html) > max_chars:
            preview += '...'
        
        return {
            'id': projeto['id'],
            'titulo': projeto['titulo'],
            'preview_html': preview,
            'tamanho_total': len(conteudo_html),
            'data_modificacao': projeto['data_modificacao']
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter preview do projeto: {e}")
        return None