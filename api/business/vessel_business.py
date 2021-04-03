from api.models.vessel_model import Vessel
from werkzeug.exceptions import Conflict
from sqlalchemy.exc import IntegrityError


class VesselBus(object):
    def __init__(self, db):
        self.db = db

    def add(self, code):
        vessel = Vessel(code=code)
        try:
            self.db.session.add(vessel)
            self.db.session.commit()
            return vessel
        except IntegrityError:
            raise Conflict("Vessel Code already exists in database")
