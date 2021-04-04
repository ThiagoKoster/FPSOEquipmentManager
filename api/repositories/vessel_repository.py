from flask_sqlalchemy import SQLAlchemy
from api.models.vessel import Vessel


class VesselRepository:
    def __init__(self, db: SQLAlchemy):
        self._db = db

    @staticmethod
    def get_all() -> [Vessel]:
        return Vessel.query.all()

    @staticmethod
    def get(vessel_id: int) -> Vessel:
        return Vessel.query.get(vessel_id)

    def add_vessel(self, vessel: Vessel) -> Vessel:
        self._db.session.add(vessel)
        self._db.session.commit()
        return vessel


