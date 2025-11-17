import psycopg2
import os
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def init_db():
    """
    Cria a tabela 'historico' no banco PostgreSQL, caso ela não exista.
    """
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Não foi possível conectar ao banco.")
            
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id SERIAL PRIMARY KEY,
            categoria TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados (PostgreSQL) inicializado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados (PostgreSQL): {e}")

def salvar_historico(categoria):
    """
    Salva um novo registro na tabela 'historico' do PostgreSQL.
    """
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Não foi possível conectar ao banco para salvar.")
            
        cursor = conn.cursor()
        
        # PostgreSQL usa %s como placeholder, NÃO usa ?.
        cursor.execute("INSERT INTO historico (categoria) VALUES (%s)", (categoria,))
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar histórico no banco de dados: {e}")

def get_dados_dashboard():
    """
    Consulta o banco PostgreSQL e retorna os dados agregados.
    """
    dados = {
        'pizza': {'produtivo': 0, 'improdutivo': 0},
        'barras': {'labels': [], 'data': []}
    }
    
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Não foi possível conectar ao banco para ler dados.")

        cursor = conn.cursor()

        # Query 1: Gráfico de Pizza (Total)
        cursor.execute("SELECT categoria, COUNT(*) FROM historico GROUP BY categoria")
        for row in cursor.fetchall():
            if row[0].lower() == 'produtivo':
                dados['pizza']['produtivo'] = row[1]
            elif row[0].lower() == 'improdutivo':
                dados['pizza']['improdutivo'] = row[1]

        # Query 2: Gráfico de Barras (Últimos 7 dias)
        # A sintaxe do PostgreSQL para datas é diferente do SQLite.
        cursor.execute("""
            SELECT DATE(criado_em) as dia, COUNT(*) 
            FROM historico 
            WHERE criado_em >= (CURRENT_DATE - INTERVAL '7 days') 
            GROUP BY dia 
            ORDER BY dia ASC
        """)
        
        for row in cursor.fetchall():
            # Converte o objeto 'date' do Python para uma string formatada
            dados['barras']['labels'].append(row[0].strftime('%Y-%m-%d'))
            dados['barras']['data'].append(row[1])

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao ler dados do dashboard: {e}")
    
    return dados