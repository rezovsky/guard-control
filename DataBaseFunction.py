from datetime import datetime, timedelta
from select import select

from models import Events
from sqlalchemy import func
from flask import jsonify


class DataBaseFunction:

    def __init__(self, db):
        self.db = db

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
            self.db.session.add(new_event)
            self.db.session.commit()

    def get_events(self, filter_group = None):
        # Вычисляем текущую дату и временной интервал для последних 7 дней
        end_date = datetime.now() #- timedelta(days=1)
        start_date = end_date - timedelta(days=14)

        # Преобразуем даты в строки в соответствии с форматом в базе данных
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Получаем список уникальных дат только за последние 7 дней
        unique_dates = self.db.session.query(Events.date).distinct().filter(Events.date >= start_date_str,
                                                                            Events.date <= end_date_str).order_by(
            Events.date).all()
        unique_dates = [datetime.strptime(date[0], '%Y-%m-%d').strftime('%d.%m') for date in unique_dates]

        # Получаем список уникальных групп
        query = self.db.session.query(Events.group).distinct().order_by(Events.group)
        if filter_group is not None:
            query = query.filter(Events.group == filter_group)

        unique_groups = query.all()
        unique_groups = [group[0] for group in unique_groups]

        # Создаем словарь для хранения количества студентов с последним статусом "вход" по группам
        count_by_group = {}

        # Перебираем группы
        for group_name in unique_groups:
            # Получаем список учеников и их последних событий за текущий день
            query = self.db.session.query(
                Events.name,
                func.json_build_object(
                    'action', Events.action,
                    'time', Events.time
                ).label('event_info')
            ).filter(
                Events.date == end_date_str,  # Фильтр по сегодняшней дате
                Events.group == group_name  # Фильтр по текущей группе
            )
            if filter_group is not None:
                query = query.filter(Events.group == filter_group)
            count_students_data = query.all()
            # Переменные для подсчета студентов с последним статусом "вход"
            count = 0

            # Перебираем учеников и их последние события
            students_events = {}
            for student in count_students_data:
                students_events[student[0]] = [dict(student[1])]
            for student, events in students_events.items():
                events_by_time = {}

                # Находим событие с максимальным временем
                for event in events:
                    event_time = event['time']
                    events_by_time[event_time] = event['action']

                sorted_events = dict(sorted(events_by_time.items(), reverse=True))
                if next(iter(sorted_events.values())) == 'вход':
                    count += 1

            # Записываем результат в словарь
            count_by_group[group_name] = count

        # Получаем список учеников с их событиями только за последние 7 дней
        query = self.db.session.query(
            Events.name,
            Events.group,
            Events.date,
            func.json_build_object(
                'action', Events.action,
                'time', Events.time
            ).label('event_info')
        ).filter(Events.date >= start_date_str, Events.date <= end_date_str).order_by(Events.name, Events.date,
                                                                                      Events.time)
        if filter_group is not None:
            query = query.filter(Events.group == filter_group)
        students_data = query.all()

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

        data = {
            'unique_dates': unique_dates,
            'unique_groups': unique_groups,
            'count_by_group': count_by_group,
            'students_info': students_info
        }

        return data
