import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),  # O nome correto do serviço no docker-compose
        database=os.getenv('DB_NAME', 'todo_db'),  # O nome do banco de dados
        user=os.getenv('DB_USER', 'postgres'),  # O usuário do banco de dados
        password=os.getenv('DB_PASS', 'postgres'),  # A senha do banco de dados
        port=5432  # A porta do PostgreSQL
    )

def init_db_postgres():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(''' 
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            status TEXT NOT NULL
        );
    ''')

    conn.commit()
    cur.close()
    conn.close()
    print("[OK] Banco de dados inicializado com sucesso!")
