from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Events(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    group = db.Column(db.String(10), nullable=False)
    action = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)