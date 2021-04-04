from api.db import db
from enum import Enum


class Status(Enum):
    ACTIVE = 1
    INACTIVE = 2


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    location = db.Column(db.String(20), nullable=False)
    vessel_id = db.Column(db.Integer, db.ForeignKey('vessel.id', ondelete="CASCADE"), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)

    def __init__(self, name, code, location, vessel_id):
        self.name = name
        self.code = code
        self.location = location
        self.vessel_id = vessel_id
        self.status = Status.ACTIVE
