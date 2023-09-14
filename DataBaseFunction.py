from models import Events


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
        events = Events.query.all()
        events_list = [event.serialize() for event in events]
        return events_list
