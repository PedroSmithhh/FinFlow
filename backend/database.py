import sqlite3
import os
from datetime import datetime

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
# Caminho normalizado para o arquivo de banco de dados (garante compatibilidade entre OS)
DB_PATH = os.path.normpath(os.path.join(DIRETORIO_ATUAL, '..', 'data', 'historico.db'))

# Garante que o diretório exista (sqlite não cria diretórios automaticamente)
DB_DIR = os.path.dirname(DB_PATH)
os.makedirs(DB_DIR, exist_ok=True)

def init_db():
    """
    Cria a tabela 'historico' no banco de dados, caso ela não exista.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        conn.commit()
        conn.close()
        print("Banco de dados inicializado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

def salvar_historico(categoria):
    """
    Salva um novo registro na tabela 'historico'.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Insere a categoria. A data é adicionada automaticamente
        cursor.execute("INSERT INTO historico (categoria) VALUES (?)", (categoria,))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar histórico no banco de dados: {e}")

def get_dados_dashboard():
    """
    Consulta o banco de dados e retorna os dados agregados para o dashboard.
    """
    dados = {
        # Dados para o gráfico de Pizza (Total)
        'pizza': {'produtivo': 0, 'improdutivo': 0},
        # Dados para o gráfico de Barras (Últimos 7 dias)
        'barras': {'labels': [], 'data': []}
    }
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Query 1: Gráfico de Pizza (Total de classificações)
        cursor.execute("SELECT categoria, COUNT(*) FROM historico GROUP BY categoria")
        for row in cursor.fetchall():
            if row[0].lower() == 'produtivo':
                dados['pizza']['produtivo'] = row[1]
            elif row[0].lower() == 'improdutivo':
                dados['pizza']['improdutivo'] = row[1]

        # Query 2: Gráfico de Barras (Volume nos últimos 7 dias)
        # Usamos a função DATE() do SQLite para agrupar por dia
        cursor.execute("""
            SELECT DATE(data) as dia, COUNT(*) 
            FROM historico 
            WHERE data >= DATE('now', '-7 days') 
            GROUP BY dia 
            ORDER BY dia ASC
        """)
        
        for row in cursor.fetchall():
            dados['barras']['labels'].append(row[0]) # Ex: '2025-11-15'
            dados['barras']['data'].append(row[1])   # Ex: 10

        conn.close()
    except Exception as e:
        print(f"Erro ao ler dados do dashboard: {e}")
    
    return dados

