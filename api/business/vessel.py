from api.models.vessel_model import Vessel
from api.db import db


class VesselBus(object):

    def add(self, code):
        vessel = Vessel(code=code)
        try:
            db.session.add(vessel)
            db.session.commit()
        except:
            return None
        return vessel
