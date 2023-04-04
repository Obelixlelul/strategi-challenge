from flask import Flask
from app.models import db
from config import populate
from app.routes import bp
from app.filters import bpf
import uuid
import os

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')

app.secret_key = uuid.uuid4().hex
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imoveisvendas.sqlite3'

# Todos os blueprints - rRotas e Filtros
app.register_blueprint(bp)
app.register_blueprint(bpf)

# Definição do caminho do banco de dados
databaseFilePath = './instance/imoveisvendas.sqlite3'

# Inicialização da aplicação
if __name__ == "__main__":
    db.init_app(app=app)
    with app.test_request_context():
        # Se não existir db, cria e o popula
        if os.path.exists(databaseFilePath):
            print(' * Database already exists')
        else:
            print(' * Database dont exists and was created')
            db.drop_all()
            db.create_all()
            populate()

    app.run(debug=True, port = 5000, host="0.0.0.0")