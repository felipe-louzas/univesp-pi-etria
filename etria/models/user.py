from flask_login import UserMixin
from etria.database import database as db


class User(UserMixin, db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    email_verified = db.Column(db.Boolean())
    password = db.Column(db.String(64))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
