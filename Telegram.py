import os
from PIL import Image, ImageDraw, ImageFont


class Telegram:
    def __init__(self, db_function):
        self.db_function = db_function
        self.border_px = 1
        self.box_px = 25
        self.folder_path = 'images'
        self.image_width = 1280
        self.image_height = 1024
        self.background_color = (255, 255, 255)

    def get_images(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        for group in self.db_function.get_unique_group():
            output_path = os.path.join(self.folder_path, f"{group}.png")

            students_data = self.db_function.get_data(group)

            dates_px = len(students_data['unique_dates']['filter_date']) * (self.box_px + self.border_px)

            font = ImageFont.truetype(os.path.join("font", "Arial.ttf"), size=18)

            name_px = 0
            text_height_px = 0
            for student in students_data['students_info'][group]:
                text_left, text_top, text_right, text_bottom = font.getbbox(student, "")
                text_width = text_left + text_right
                text_height = text_top + text_bottom
                text_height_px = max(text_height_px, text_height)
                name_px = max(name_px, text_width) + 5

            self.image_width = name_px + dates_px

            # Создайте изображение и холст

            image = Image.new("RGB", (self.image_width, self.image_height), "white")
            draw = ImageDraw.Draw(image)

            # Рисуем горизонтальные линии таблицы
            for i in range(len(students_data['students_info'][group]) + 1):
                y = i * self.box_px
                draw.line([(0, y), (self.image_width, y)], fill="black")

            # Рисуем вертикальные линии таблицы
            for i in range(len(students_data['unique_dates']['filter_date']) + 1):
                x = i * self.box_px
                draw.line([(x, 0), (x, self.image_height)], fill="black")

            # Заполняем ячейки таблицы данными
            for row, student_name in enumerate(student):
                for col, date in enumerate(students_data['unique_dates']['filter_date']):
                    # Определите цвет для ячейки в соответствии с вашей логикой
                    color = "green"  # Замените на свой цвет

                    # Рисуем квадрат
                    x0 = col * self.box_px
                    y0 = row * self.box_px
                    x1 = x0 + self.box_px
                    y1 = y0 + self.box_px
                    draw.rectangle([x0, y0, x1, y1], fill=color)

                    # Рисуем текст (имя студента) в центре ячейки
                    text_x = (x0 + x1) / 2
                    text_y = (y0 + y1) / 2
                    draw.text((text_x, text_y), student_name, fill="black", font=font)

            # Сохраняем изображение
            image.save(output_path)

        return 'ok'
