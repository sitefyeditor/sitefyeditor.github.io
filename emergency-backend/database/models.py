"""
Emergency Backend - Modelos de Dados
Define a estrutura das tabelas usuarios e projetos
"""

from database.db import execute_query
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Usuario:
    """Modelo para gerenciar usuários do sistema"""
    
    def __init__(self, id=None, nome=None, email=None, senha_hash=None, 
                 data_criacao=None, ultima_atividade=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.data_criacao = data_criacao
        self.ultima_atividade = ultima_atividade
    
    @staticmethod
    def criar_usuario(nome, email, senha):
        """
        Cria um novo usuário no banco de dados
        
        Args:
            nome (str): Nome do usuário
            email (str): Email do usuário
            senha (str): Senha em texto puro (será criptografada)
        
        Returns:
            dict: Dados do usuário criado ou None se erro
        """
        try:
            # Verificar se email já existe
            usuario_existente = Usuario.buscar_por_email(email)
            if usuario_existente:
                return None
            
            # Criptografar senha
            senha_hash = generate_password_hash(senha)
            
            # Inserir usuário
            cursor = execute_query(
                """
                INSERT INTO usuarios (nome, email, senha_hash) 
                VALUES (?, ?, ?)
                """,
                (nome, email, senha_hash)
            )
            
            usuario_id = cursor.lastrowid
            
            # Buscar usuário criado
            return Usuario.buscar_por_id(usuario_id)
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            return None
    
    @staticmethod
    def buscar_por_email(email):
        """
        Busca usuário por email
        
        Args:
            email (str): Email do usuário
        
        Returns:
            dict: Dados do usuário ou None se não encontrado
        """
        try:
            return execute_query(
                "SELECT * FROM usuarios WHERE email = ?",
                (email,),
                fetch_one=True
            )
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por email: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(usuario_id):
        """
        Busca usuário por ID
        
        Args:
            usuario_id (int): ID do usuário
        
        Returns:
            dict: Dados do usuário ou None se não encontrado
        """
        try:
            return execute_query(
                "SELECT * FROM usuarios WHERE id = ?",
                (usuario_id,),
                fetch_one=True
            )
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por ID: {e}")
            return None
    
    @staticmethod
    def verificar_senha(email, senha):
        """
        Verifica se a senha está correta para um usuário
        
        Args:
            email (str): Email do usuário
            senha (str): Senha em texto puro
        
        Returns:
            dict: Dados do usuário se senha correta, None caso contrário
        """
        try:
            usuario = Usuario.buscar_por_email(email)
            if not usuario:
                return None
            
            if check_password_hash(usuario['senha_hash'], senha):
                # Atualizar última atividade
                Usuario.atualizar_ultima_atividade(usuario['id'])
                return usuario
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao verificar senha: {e}")
            return None
    
    @staticmethod
    def atualizar_ultima_atividade(usuario_id):
        """
        Atualiza o timestamp da última atividade do usuário
        
        Args:
            usuario_id (int): ID do usuário
        """
        try:
            execute_query(
                "UPDATE usuarios SET ultima_atividade = CURRENT_TIMESTAMP WHERE id = ?",
                (usuario_id,)
            )
        except Exception as e:
            logger.error(f"Erro ao atualizar última atividade: {e}")
    
    @staticmethod
    def listar_todos():
        """
        Lista todos os usuários do sistema (para debug)
        
        Returns:
            list: Lista de usuários
        """
        try:
            return execute_query(
                "SELECT id, nome, email, data_criacao, ultima_atividade FROM usuarios",
                fetch_all=True
            )
        except Exception as e:
            logger.error(f"Erro ao listar usuários: {e}")
            return []

class Projeto:
    """Modelo para gerenciar projetos HTML dos usuários"""
    
    def __init__(self, id=None, usuario_id=None, titulo=None, conteudo_html=None,
                 data_criacao=None, data_modificacao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.conteudo_html = conteudo_html
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao
    
    @staticmethod
    def criar_projeto(usuario_id, titulo, conteudo_html):
        """
        Cria um novo projeto para um usuário
        
        Args:
            usuario_id (int): ID do usuário proprietário
            titulo (str): Título do projeto
            conteudo_html (str): Conteúdo HTML do projeto
        
        Returns:
            dict: Dados do projeto criado ou None se erro
        """
        try:
            cursor = execute_query(
                """
                INSERT INTO projetos (usuario_id, titulo, conteudo_html) 
                VALUES (?, ?, ?)
                """,
                (usuario_id, titulo, conteudo_html)
            )
            
            projeto_id = cursor.lastrowid
            return Projeto.buscar_por_id(projeto_id)
            
        except Exception as e:
            logger.error(f"Erro ao criar projeto: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(projeto_id):
        """Busca projeto por ID"""
        try:
            return execute_query(
                "SELECT * FROM projetos WHERE id = ?",
                (projeto_id,),
                fetch_one=True
            )
        except Exception as e:
            logger.error(f"Erro ao buscar projeto por ID: {e}")
            return None
    
    @staticmethod
    def listar_por_usuario(usuario_id):
        """
        Lista todos os projetos de um usuário
        
        Args:
            usuario_id (int): ID do usuário
        
        Returns:
            list: Lista de projetos do usuário
        """
        try:
            return execute_query(
                """
                SELECT id, titulo, data_criacao, data_modificacao,
                       LENGTH(conteudo_html) as tamanho_html
                FROM projetos 
                WHERE usuario_id = ?
                ORDER BY data_modificacao DESC
                """,
                (usuario_id,),
                fetch_all=True
            )
        except Exception as e:
            logger.error(f"Erro ao listar projetos do usuário: {e}")
            return []
    
    @staticmethod
    def atualizar_projeto(projeto_id, titulo=None, conteudo_html=None):
        """
        Atualiza um projeto existente
        
        Args:
            projeto_id (int): ID do projeto
            titulo (str, opcional): Novo título
            conteudo_html (str, opcional): Novo conteúdo HTML
        
        Returns:
            dict: Projeto atualizado ou None se erro
        """
        try:
            # Buscar projeto atual
            projeto = Projeto.buscar_por_id(projeto_id)
            if not projeto:
                return None
            
            # Preparar valores para atualização
            novo_titulo = titulo if titulo is not None else projeto['titulo']
            novo_conteudo = conteudo_html if conteudo_html is not None else projeto['conteudo_html']
            
            # Atualizar no banco
            execute_query(
                """
                UPDATE projetos 
                SET titulo = ?, conteudo_html = ?, data_modificacao = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (novo_titulo, novo_conteudo, projeto_id)
            )
            
            return Projeto.buscar_por_id(projeto_id)
            
        except Exception as e:
            logger.error(f"Erro ao atualizar projeto: {e}")
            return None
    
    @staticmethod
    def deletar_projeto(projeto_id, usuario_id):
        """
        Deleta um projeto (verificando se pertence ao usuário)
        
        Args:
            projeto_id (int): ID do projeto
            usuario_id (int): ID do usuário (para verificação)
        
        Returns:
            bool: True se deletado, False caso contrário
        """
        try:
            # Verificar se o projeto pertence ao usuário
            projeto = execute_query(
                "SELECT id FROM projetos WHERE id = ? AND usuario_id = ?",
                (projeto_id, usuario_id),
                fetch_one=True
            )
            
            if not projeto:
                return False
            
            # Deletar projeto
            execute_query(
                "DELETE FROM projetos WHERE id = ? AND usuario_id = ?",
                (projeto_id, usuario_id)
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar projeto: {e}")
            return False
    
    @staticmethod
    def contar_projetos_usuario(usuario_id):
        """
        Conta quantos projetos um usuário possui
        
        Args:
            usuario_id (int): ID do usuário
        
        Returns:
            int: Número de projetos
        """
        try:
            result = execute_query(
                "SELECT COUNT(*) as count FROM projetos WHERE usuario_id = ?",
                (usuario_id,),
                fetch_one=True
            )
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Erro ao contar projetos: {e}")
            return 0