from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    group = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(5), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'name': self.name,
            'group': self.group,
            'action': self.action,
            'time': self.time
        }