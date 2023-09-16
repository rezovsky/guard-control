from flask import Flask, jsonify, render_template, request
from flask_migrate import Migrate

from DataBaseFunction import DataBaseFunction
from Telegram import Telegram
from XlsImport import XlsImport
from models import db

app = Flask(__name__)

db_user = "guard"
db_password = "12345"
db_name = "guard"
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost/{db_name}'

db.init_app(app)

migrate = Migrate(app, db)

db_function = DataBaseFunction(db)

tg = Telegram()


@app.route('/import', methods=['GET'])
def import_xls():
    xlsimport = XlsImport('_xls', db)
    return jsonify(xlsimport.xls_import())


@app.route('/get_data', methods=['GET'])
def get_data():
    events = db_function.get_events()
    return (jsonify(events))


@app.route('/get_data/<string:group>', methods=['GET'])
def get_data_from_group(group):
    events = db_function.get_events(group)
    return jsonify(events)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/telegram/get_images', methods=['GET'])
def get_images():
    base_url = request.url_root
    groups = db_function.get_unique_group()
    return tg.get_images(groups, base_url)

@app.route('/group/<string:group>', methods=['GET'])
def group_page(group):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
