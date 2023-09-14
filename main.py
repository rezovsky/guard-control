from flask import Flask, jsonify, render_template

from DB import DB
from XlsImport import XlsImport

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/db'

db = DB(app)


@app.route('/get_data', methods=['GET'])
def get_data():
    xlsimport = XlsImport('_xls')
    return jsonify(xlsimport.xls_import())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
