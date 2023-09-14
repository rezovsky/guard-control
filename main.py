import os

from flask import Flask, jsonify, render_template

from DB import DB
from XlsImport import XlsImport

app = Flask(__name__)

db_file = os.path.join(os.path.dirname(__file__), 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'

db = DB(app)


@app.route('/get_data', methods=['GET'])
def get_data():
    xlsimport = XlsImport('_xls', db)
    return jsonify(xlsimport.xls_import())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
