

from app import create_app
from app.db.mssql import init_db
from app.db.postgressql import init_db_postgres

app = create_app()

if __name__ == "__main__":
    init_db()  # Inicializa as tabelas se ainda não existirem
    init_db_postgres()  # Inicializa as tabelas se ainda não existirem
    app.run(host="0.0.0.0", port=80, debug=True)
