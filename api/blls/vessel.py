from werkzeug.exceptions import Conflict
from sqlalchemy.exc import IntegrityError
from api.models.vessel import Vessel
from api.repositories.vessel import VesselRepository


class VesselBus(object):
    def __init__(self, vessel_repository: VesselRepository):
        self.vessel_repository = vessel_repository

    def add(self, code):
        try:
            return self.vessel_repository.add_vessel(Vessel(code=code))
        except IntegrityError:
            raise Conflict("Vessel Code already exists in database")

    def get_vessels(self):
        return self.vessel_repository.get_all()
