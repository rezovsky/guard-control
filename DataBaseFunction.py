from datetime import datetime, timedelta

from models import Events
from sqlalchemy import func


class DataBaseFunction:

    def __init__(self, db):
        self.now_date_str = None
        self.start_date_str = None
        self.filter_group = None
        self.db = db
        self.days_interval = 14

        self.get_now_date()

    def add_event(self, data):
        existing_event = Events.query.filter_by(
            date=data['date'],
            name=data['name'],
            group=data['group'],
            action=data['action'],
            time=data['time']
        ).first()

        if existing_event is None:
            new_event = Events(**data)
            print(data)
            self.db.session.add(new_event)
            self.db.session.commit()

    def get_data(self, filter_group=None):
        self.get_now_date()
        self.filter_group = filter_group
        data = {
            'unique_dates': self.get_unique_dates(),
            'unique_groups': self.get_unique_group(),
            'count_by_group': self.get_entered_from_group(),
            'students_info': self.get_students_events()
        }
        return data

    def get_entered_from_group(self):
        # Создаем словарь для хранения количества студентов с последним статусом "вход" по группам
        count_by_group = {}

        # Перебираем группы
        for group_name, group_events in self.get_status_by_group_of_date(self.now_date_str).items():
            # Переменные для подсчета студентов с последним статусом "вход"
            count = 0
            for event in group_events.values():
                if event == 'вход':
                    count += 1

            # Записываем результат в словарь
            count_by_group[group_name] = count
        return count_by_group

    def get_status_by_group_of_date(self, date_str):
        status_by_group = {}

        # Перебираем группы
        for group_name in self.get_unique_group():
            # Получаем список учеников и их последних событий за текущий день
            query = self.get_students().filter(
                Events.date == date_str,  # Фильтр по дате
                Events.group == group_name  # Фильтр по текущей группе
            )
            status_students_data = self.group_filter(query)

            # Перебираем учеников и их последние события
            students_event = {}
            for student in status_students_data:
                students_event[student[0]] = student[3]['action']
            status_by_group[group_name] = students_event
        return status_by_group

    def get_students_events(self):
        # Получаем список учеников с их событиями
        query = self.get_students().filter(Events.date >= self.start_date_str,
                                           Events.date <= self.now_date_str).order_by(Events.name,
                                                                                      Events.date, Events.time)
        students_data = self.group_filter(query)

        students_info = {}

        for student in students_data:
            student_name = student[0]
            group_name = student[1]
            event_date = datetime.strptime(student[2], '%Y-%m-%d').strftime('%d.%m')
            action = student[3]['action']
            time = student[3]['time']

            if group_name not in students_info:
                students_info[group_name] = {}

            if student_name not in students_info[group_name]:
                students_info[group_name][student_name] = {}

            if event_date not in students_info[group_name][student_name]:
                students_info[group_name][student_name][event_date] = []

            students_info[group_name][student_name][event_date].append({
                'action': action,
                'time': time
            })
        return students_info

    def get_unique_group(self):
        # Получаем список уникальных групп
        query = self.db.session.query(Events.group).distinct().order_by(Events.group)
        unique_groups = [group[0] for group in self.group_filter(query)]
        return unique_groups

    def get_unique_dates(self):
        unique_dates = self.db.session.query(Events.date).distinct().filter(Events.date >= self.start_date_str,
                                                                            Events.date <= self.now_date_str).order_by(
            Events.date).all()
        unique_dates = {
            'text_date': [datetime.strptime(date[0], '%Y-%m-%d').strftime('%d.%m') for date in unique_dates],
            'filter_date': [datetime.strptime(date[0], '%Y-%m-%d').strftime('%Y-%m-%d') for date in unique_dates]
        }
        return unique_dates

    def get_students(self):
        return self.db.session.query(
            Events.name,
            Events.group,
            Events.date,
            func.json_build_object(
                'action', Events.action,
                'time', Events.time
            ).label('event_info')
        )

    def group_filter(self, query):
        if self.filter_group is not None:
            query = query.filter(Events.group == self.filter_group)
        return query.all()

    def get_now_date(self):
        # Вычисляем текущую дату и временной интервал
        now_date = datetime.now()  # - timedelta(days=1)  # это нужно для ночной разработки, когда уже наступило завтра
        start_date = now_date - timedelta(days=self.days_interval)

        # Преобразуем даты в строки в соответствии с форматом в базе данных
        self.start_date_str = start_date.strftime('%Y-%m-%d')
        self.now_date_str = now_date.strftime('%Y-%m-%d')
