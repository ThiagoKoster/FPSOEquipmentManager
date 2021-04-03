from werkzeug.exceptions import NotFound
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError
from api.models.vessel_model import Vessel
from api.models.equipment_model import Equipment, Status


class EquipmentBus(object):
    def __init__(self, db):
        self.db = db

    def add_equipment(self, vessel_id, equipment):
        self._validate_vessel_id(vessel_id)
        equipment = Equipment(equipment.name, equipment.code, equipment.location, vessel_id)
        try:
            self.db.session.add(equipment)
            self.db.session.commit()
            return equipment
        except IntegrityError:
            raise Conflict(f'Equipment code {equipment.code} already in use')

    def get_vessel_equipments(self, vessel_id, status):
        self._validate_vessel_id(vessel_id)
        if status is None:
            return self.dal_get_vessel_equipments(vessel_id)
        status_enum = self._validate_status(status)
        equipments = self.dal_get_vessel_equipments_with_status(vessel_id, status_enum)
        return equipments

    def _validate_vessel_id(self, vessel_id):
        vessel = self.get(vessel_id)
        if vessel is None:
            raise NotFound(f'Vessel with id {vessel_id} not found')

    @staticmethod
    def dal_get_vessel_equipments(vessel_id):
        return Equipment.query.filter(Equipment.vessel_id == vessel_id).all()

    @staticmethod
    def dal_get_vessel_equipments_with_status(vessel_id, status):
        return Equipment.query.filter(Equipment.vessel_id == vessel_id, Equipment.status == status).all()

    @staticmethod
    def get(vessel_id):
        return Vessel.query.get(vessel_id)

    @staticmethod
    def _validate_status(status):
        try:
            status_enum = Status[status.upper()]
        except KeyError:
            raise BadRequest(f'Invalid status: {status}')
        return status_enum
