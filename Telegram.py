import os
from PIL import Image, ImageDraw, ImageFont


class Telegram:
    def __init__(self, db_function):
        self.db_function = db_function
        self.border_px = 1
        self.text_padding = 6
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

            dates = students_data['unique_dates']['filter_date']
            dates_px = len(dates) * (self.box_px + (self.border_px * 2))

            font = ImageFont.truetype(os.path.join("font", "Arial.ttf"), size=18)

            name_px = 0
            name_height_px = 0
            for student in students_data['students_info'][group]:
                text_left, text_top, text_right, text_bottom = font.getbbox(student, "")
                text_width = text_right - text_left
                name_px = max(name_px, text_width)
                name_height_px += self.box_px

            name_px += self.text_padding
            self.image_width = name_px + dates_px - self.border_px
            self.image_height = name_height_px + self.box_px

            # Создайте изображение и холст

            image = Image.new("RGB", (self.image_width, self.image_height), "white")
            draw = ImageDraw.Draw(image)

            students_list = []
            # Рисуем горизонтальные линии таблицы
            for index, student in enumerate(students_data['students_info'][group], start=1):
                y = index * self.box_px + self.border_px
                draw.line([(0, y), (self.image_width, y)], fill="black")

                # Рисуем текст (имя студента) в центре ячейки
                text_x = self.text_padding
                text_y = y + (self.text_padding / 2)
                draw.text((text_x, text_y), student, fill="black", font=font)
                students_list.append(student)

            # Рисуем вертикальные линии таблицы
            for index, date in enumerate(students_data['unique_dates']['filter_date'], start=0):
                x = index * (self.box_px + self.border_px) + name_px + self.text_padding + self.border_px
                draw.line([(x, 0), (x, self.image_height)], fill="black")

                status_list = self.db_function.get_status_by_group_of_date(date)[group]
                for row_number, student in enumerate(students_list, start=1):
                    if student in status_list:
                        status = status_list[student]
                        if status == 'выход':
                            color = 'red'
                        else:
                            color = 'green'
                    else:
                        color = 'gray'

                    x0 = x + self.border_px
                    y0 = row_number * self.box_px + (self.border_px * 2)
                    x1 = x0 + self.box_px
                    y1 = y0 + self.box_px - (self.border_px * 2)
                    draw.rectangle([x0, y0, x1, y1], fill=color)

            # Сохраняем изображение
            image.save(output_path)

        return 'ok'
