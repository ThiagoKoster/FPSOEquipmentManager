from api.db import db


class Vessel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    equipments = db.relationship('Equipment', backref='vessel')

    def __init__(self, code):
        self.code = code
