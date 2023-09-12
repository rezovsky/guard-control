from flask import Flask, jsonify, render_template
import os
import xlrd
from collections import defaultdict

app = Flask(__name__)


@app.route('/get_data', methods=['GET'])
def get_data():
    # Указываем путь к папке, в которой находятся файлы XLS
    folder_path = "xls"

    # Получаем список файлов в папке
    files = os.listdir(folder_path)

    # Перебираем файлы и выбираем первый файл с расширением .xls
    for file in files:
        if file.endswith(".xls"):
            file_path = os.path.join(folder_path, file)
            break
    else:
        print("Файлы XLS не найдены в папке")
        exit()

    # Открываем файл XLS
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)

    # Создаем словарь для хранения данных
    data_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    # Индексы столбцов, которые вы хотите использовать для формирования словаря
    date_col_index = 0
    class_col_index = 1
    name_col_index = 2
    # Пропускаем столбец с табельным номером (не используется)
    time_col_index = 4
    action_col_index = 6

    # Переменная для хранения данных предыдущей строки
    previous_row_data = None

    # Проходим по строкам листа, начиная с 7-й строки, и формируем словарь
    for row_num in range(8, sheet.nrows):
        row = sheet.row_values(row_num)

        # Проверяем, все ли значения в первых 4 колонках пустые
        if all(cell == "" for cell in row[:4]):
            # Если все пустые, используем данные из предыдущей строки
            row[:4] = previous_row_data[:4]

        date = row[date_col_index]
        class_name = row[class_col_index]
        name = row[name_col_index]
        time = row[time_col_index]
        action = row[action_col_index]

        if date and class_name and name and time and action:
            data_dict[class_name][name][date][time] = action

        # Сохраняем данные текущей строки для использования в следующей
        previous_row_data = row
    return jsonify(data_dict)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
