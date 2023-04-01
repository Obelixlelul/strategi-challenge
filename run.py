from flask import Flask
from app.models import db
from config import populate
from app.routes import bp
import uuid
import os
import locale

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')
app.secret_key = uuid.uuid4().hex
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imoveisvendas.sqlite3'

# all my routes
app.register_blueprint(bp)


databaseFilePath = './instance/imoveisvendas.sqlite3'

if __name__ == "__main__":
    db.init_app(app=app)
    with app.test_request_context():
        # delete database, create new tables and populate with data if database not exists
        # if os.path.exists(databaseFilePath):
        #     print(' * Database already exists')
        # else:
        #     print(' * Database dont exists and was created')
            db.drop_all()
            db.create_all()
            populate()

    app.run(debug=True, port = 5000)