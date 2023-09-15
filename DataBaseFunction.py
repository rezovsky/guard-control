from datetime import datetime, timedelta

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

    def get_all_events(self):
        # Вычисляем текущую дату и временной интервал для последних 7 дней
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Преобразуем даты в строки в соответствии с форматом в базе данных
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

        # Получаем список уникальных дат только за последние 7 дней
        unique_dates = self.db.session.query(Events.date).distinct().filter(Events.date >= start_date_str,
                                                                            Events.date <= end_date_str).order_by(
            Events.date).all()
        unique_dates = [datetime.strptime(date[0], '%Y-%m-%d').strftime('%d.%m') for date in unique_dates]
        # Получаем список уникальных групп
        unique_groups = self.db.session.query(Events.group).distinct().order_by(Events.group).all()
        unique_groups = [group[0] for group in unique_groups]

        # Получаем список учеников с их событиями только за последние 7 дней
        students_data = self.db.session.query(
            Events.name,
            Events.group,
            Events.date,
            func.json_build_object(
                'action', Events.action,
                'time', Events.time
            ).label('event_info')
        ).filter(Events.date >= start_date_str, Events.date <= end_date_str).order_by(Events.name, Events.date,
                                                                                      Events.time).all()

        students_info = {}

        for student in students_data:
            print(student)
            student_name = student[0]
            group_name = student[1]
            event_date = student[2]
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
            'students_info': students_info
        }

        return data
