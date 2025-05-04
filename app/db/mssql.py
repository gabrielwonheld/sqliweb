import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sqlserver;"
    "DATABASE=master;"
    "UID=sa;"
    "PWD=YourStrong!Passw0rd"
)

def get_connection():
    return pyodbc.connect(conn_str)

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
            CREATE TABLE users (
                id INT IDENTITY(1,1) PRIMARY KEY,
                username NVARCHAR(255) UNIQUE NOT NULL,
                password NVARCHAR(255) NOT NULL,
                email NVARCHAR(255) NOT NULL
            )
        ''')

        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='goals' AND xtype='U')
            CREATE TABLE goals (
                id INT IDENTITY(1,1) PRIMARY KEY,
                user_id INT,
                title NVARCHAR(255),
                productivity_score INT,
                pomodoro_count INT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
    except Exception as e:
        print("[ERRO] Falha ao criar tabelas:", e)
    finally:
        conn.close()
