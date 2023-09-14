from flask import Flask, jsonify, render_template
from flask_migrate import Migrate

from DataBaseFunction import DataBaseFunction
from XlsImport import XlsImport
from models import db

app = Flask(__name__)

db_user = "guard"
db_password = "12345"
db_name = "guard"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost/{db_name}'

db.init_app(app)

migrate = Migrate(app, db)


@app.route('/import', methods=['GET'])
def importXls():
    xlsimport = XlsImport('_xls', db)
    return jsonify(xlsimport.xls_import())


@app.route('/get_data', methods=['GET'])
def get_data():
    db_function = DataBaseFunction(db)
    events = db_function.get_all_events()
    return jsonify(events)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
