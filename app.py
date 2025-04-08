from flask import * #importing flask (Install it using python -m pip install flask)
import pyodbc

app = Flask(__name__) #initialising flask
app.secret_key = 'chave_supersecreta'  # use algo forte em produção


@app.route("/") #defining the routes for the home() funtion (Multiple routes can be used as seen here)
@app.route("/home")
def home():
    return render_template("home.html") #rendering our home.html contained within /templates


# Configuração da conexão MSSQL
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sqlserver;"  # Nome do container MSSQL ou IP
    "DATABASE=master;"   # Ou outro database criado
    "UID=sa;"
    "PWD=YourStrong!Passw0rd"
)

# Cria a tabela (uma vez só)
def init_db():
    try:
        conn = pyodbc.connect(conn_str)
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
        conn.commit()
        conn.close()
    except Exception as e:
        print("Erro ao criar tabela:", e)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            conn.commit()
            return redirect(url_for('login'))
        except pyodbc.IntegrityError:
            return "Usuário já existe!"
        except Exception as e:
            return f"Erro: {e}"
        finally:
            conn.close()
    return render_template('register.html')


"""Conta"""
@app.route("/account", methods=["POST", "GET"]) #defining the routes for the account() funtion
def account():
    
    if "username" not in session:
        print('não tem')
        return redirect(url_for('login'))
    usr = request.args.get("username", "<User Not Defined>")
    return render_template("account.html", username=session['username']) #



"""login"""
@app.route("/login",methods=["GET","POST"])
def login():

    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:

            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            # VULNERÁVEL A SQL INJECTION!
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            print("[DEBUG] Query:", query)
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                session["username"] = username
                return redirect(url_for('account'))
            else:
                return "<h3>Credenciais inválidas.</h3>", 403
        except Exception as e:
            return f"<h3>Erro: {str(e)}</h3>", 500
        finally:
            conn.close()
    return render_template('login.html',error=error)



"""Pomodoro"""
@app.route("/pomodoro",methods=["GET"])
def pomodoro():
    return render_template("pomodoro.html")


if __name__ == "__main__": #checking if __name__'s value is '__main__'. __name__ is an python environment variable who's value will always be '__main__' till this is the first instatnce of app.py running
    init_db()
    app.run(host='0.0.0.0',debug=True,port=80) #running flask (Initalised on line 4)
