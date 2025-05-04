from flask import Flask
from app.auth.auth import auth_bp
from app.routes.goals_mssql import goals_bp
from app.routes.home import home_bp
from app.routes.todo_postgress import todo_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",  # relativo ao diretório atual (__name__)
        static_folder="static"
    )

    app.secret_key = 'chave_supersecreta'

    app.register_blueprint(auth_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(todo_bp)

    '''print(app.url_map)
    print('oi')'''
    
    '''for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule}")'''
    
    return app
