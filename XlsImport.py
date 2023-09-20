import os
from collections import defaultdict

import xlrd
from DataBaseFunction import DataBaseFunction


class XlsImport:
    def __init__(self, folder_path, db):
        self.folder_path = folder_path
        self.db = db
        self.db_function = DataBaseFunction(db)

    def xls_import(self):

        # Получаем список файлов в папке
        files = os.listdir(self.folder_path)

        # Перебираем файлы и выбираем первый файл с расширением ._xls
        for file in files:
            if file.endswith(".xls"):
                file_path = os.path.join(self.folder_path, file)
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
        time_col_index = 4
        action_col_index = 6

        previous_row_data = None

        # Проходим по строкам листа, начиная с 8-й строки, и формируем словарь
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
                event = {
                    'date': date,
                    'name': name,
                    'group': class_name,
                    'action': action,
                    'time': time
                }
                self.db_function.add_event(event)

            previous_row_data = row

        return 'ok'
