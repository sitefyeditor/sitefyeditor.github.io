"""
Emergency Backend - Gerenciador de Banco de Dados
Responsável pela conexão e inicialização do SQLite
"""

import sqlite3
import threading
from pathlib import Path
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

# Thread-local storage para conexões SQLite
_local = threading.local()

def get_db_connection():
    """
    Obtém uma conexão com o banco de dados
    Usa thread-local storage para segurança em threading
    """
    if not hasattr(_local, 'connection'):
        # Garantir que o diretório existe
        Config.ensure_database_directory()
        
        # Criar conexão
        _local.connection = sqlite3.connect(
            str(Config.DATABASE_PATH),
            timeout=30.0,
            check_same_thread=False
        )
        
        # Configurar row factory para dicionários
        _local.connection.row_factory = sqlite3.Row
        
        # Habilitar foreign keys
        _local.connection.execute("PRAGMA foreign_keys = ON")
        
        logger.info(f"Nova conexão estabelecida: {Config.DATABASE_PATH}")
    
    return _local.connection

def close_db_connection():
    """Fecha a conexão atual se existir"""
    if hasattr(_local, 'connection'):
        _local.connection.close()
        delattr(_local, 'connection')
        logger.info("Conexão com banco fechada")

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Executa uma query no banco de dados
    
    Args:
        query (str): SQL query para executar
        params (tuple): Parâmetros para a query
        fetch_one (bool): Se deve retornar apenas um resultado
        fetch_all (bool): Se deve retornar todos os resultados
    
    Returns:
        Resultado da query ou cursor
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            result = cursor.fetchone()
            return dict(result) if result else None
        elif fetch_all:
            results = cursor.fetchall()
            return [dict(row) for row in results]
        else:
            conn.commit()
            return cursor
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao executar query: {e}")
        raise
    finally:
        cursor.close()

def init_database():
    """
    Inicializa o banco de dados criando todas as tabelas necessárias
    """
    logger.info("Inicializando banco de dados...")
    
    # Garantir que o diretório existe
    Config.ensure_database_directory()
    
    # Queries de criação das tabelas
    create_tables_queries = [
        # Tabela de usuários
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            senha_hash VARCHAR(255) NOT NULL,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            ultima_atividade DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """,
        
        # Tabela de projetos
        """
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            conteudo_html TEXT NOT NULL,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_modificacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
        )
        """,
        
        # Índices para melhor performance
        """
        CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)
        """,
        
        """
        CREATE INDEX IF NOT EXISTS idx_projetos_usuario ON projetos(usuario_id)
        """,
        
        """
        CREATE INDEX IF NOT EXISTS idx_projetos_titulo ON projetos(titulo)
        """
    ]
    
    # Executar queries de criação
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        for query in create_tables_queries:
            cursor.execute(query)
        
        conn.commit()
        logger.info("Banco de dados inicializado com sucesso!")
        
        # Verificar se existem tabelas
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        
        tables = cursor.fetchall()
        logger.info(f"Tabelas criadas: {[table['name'] for table in tables]}")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao inicializar banco: {e}")
        raise
    finally:
        cursor.close()

def get_database_info():
    """Retorna informações sobre o banco de dados"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Contar usuários
        cursor.execute("SELECT COUNT(*) as count FROM usuarios")
        usuarios_count = cursor.fetchone()['count']
        
        # Contar projetos
        cursor.execute("SELECT COUNT(*) as count FROM projetos") 
        projetos_count = cursor.fetchone()['count']
        
        # Tamanho do arquivo do banco
        db_size = Config.DATABASE_PATH.stat().st_size if Config.DATABASE_PATH.exists() else 0
        
        cursor.close()
        
        return {
            "database_path": str(Config.DATABASE_PATH),
            "usuarios_total": usuarios_count,
            "projetos_total": projetos_count,
            "tamanho_db_bytes": db_size,
            "tamanho_db_mb": round(db_size / (1024 * 1024), 2)
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter informações do banco: {e}")
        return None