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
        # Получаем список уникальных дат
        unique_dates = self.db.session.query(Events.date).distinct().all()

        # Получаем список уникальных групп
        unique_groups = self.db.session.query(Events.group).distinct().all()

        # Получаем список учеников с их датами и направлением прохода
        students_data = self.db.session.query(
            Events.name,
            Events.group,
            Events.date,
            func.array_agg(func.json_build_object('action', Events.action, 'time', Events.time)).label('events')
        ).group_by(Events.name, Events.group, Events.date).all()

        # Преобразуем результаты в нужный формат
        unique_dates = [date[0] for date in unique_dates]
        unique_groups = [group[0] for group in unique_groups]
        students_info = []

        for student in students_data:
            student_info = {
                'name': student.name,
                'group': student.group,
                'events': student.events,
            }
            students_info.append(student_info)

        data = {
            'unique_dates': unique_dates,
            'unique_groups': unique_groups,
            'students_info': students_info,
        }

        return data
