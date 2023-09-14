from flask_sqlalchemy import SQLAlchemy

from model import Events


class DB:
    db = SQLAlchemy()

    def __init__(self, app):
        self.db.init_app(app)
        with app.app_context():
            self.db.create_all()

    def add_event(self, **kwargs):
        new_user = Events(**kwargs)
        self.db.session.add(new_user)
        self.db.session.commit()

    def get_all_events(self):
        return Events.query.all()
