import os
from PIL import Image, ImageDraw, ImageFont

class Telegram:
    def __init__(self, db_function):
        self.db_function = db_function

    def get_images(self):
        folder_path = 'images'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for group in self.db_function.get_unique_group():
            output_path = f"{folder_path}/{group}.png"

            # Создайте изображение и холст
            width = 1280  # Ширина изображения
            height = 1024  # Высота изображения
            image = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(image)

            # Шрифт для текста
            font = ImageFont.load_default()

            # Размеры ячеек таблицы
            cell_width = 25
            cell_height = 25

            # Список дат и имен
            dates = ["01.09", "02.09", "03.09"]
            students_names = ["Student 1", "Student 2", "Student 3"]

            # Рисуем горизонтальные линии таблицы
            for i in range(len(students_names) + 1):
                y = i * cell_height
                draw.line([(0, y), (width, y)], fill="black")

            # Рисуем вертикальные линии таблицы
            for i in range(len(dates) + 1):
                x = i * cell_width
                draw.line([(x, 0), (x, height)], fill="black")

            # Заполняем ячейки таблицы данными
            for row, student_name in enumerate(students_names):
                for col, date in enumerate(dates):
                    # Определите цвет для ячейки в соответствии с вашей логикой
                    color = "green"  # Замените на свой цвет

                    # Рисуем квадрат
                    x0 = col * cell_width
                    y0 = row * cell_height
                    x1 = x0 + cell_width
                    y1 = y0 + cell_height
                    draw.rectangle([x0, y0, x1, y1], fill=color)

                    # Рисуем текст (имя студента) в центре ячейки
                    text_x = (x0 + x1) / 2
                    text_y = (y0 + y1) / 2
                    draw.text((text_x, text_y), student_name, fill="black", font=font)

            # Сохраняем изображение
            image.save(output_path)

        return 'ok'
