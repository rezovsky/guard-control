from flask import Flask, jsonify, render_template
import os
import xlrd
from collections import defaultdict

from XlsImport import XlsImport

app = Flask(__name__)


@app.route('/get_data', methods=['GET'])
def get_data():
    xlsimport = XlsImport('xls')
    return jsonify(xlsimport.xls_import())


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
