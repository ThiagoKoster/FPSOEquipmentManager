from werkzeug.exceptions import NotFound
from werkzeug.exceptions import Conflict
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError
from api.models.vessel import Vessel
from api.models.equipment import Equipment, Status
from api.repositories.equipment import EquipmentRepository
from api.repositories.vessel import VesselRepository


class EquipmentBus(object):
    def __init__(self, vessel_repository: VesselRepository, equipment_repository: EquipmentRepository):
        self._vessel_repo = vessel_repository
        self._equipment_repo = equipment_repository

    def add_equipment(self, vessel_id, equipments_dict):
        self._validate_vessel_id(vessel_id)
        equipments = [Equipment(e['name'], e['code'], e['location'], vessel_id) for e in equipments_dict]
        try:
            return self._equipment_repo.add(equipments)
        except IntegrityError as e:
            raise Conflict(f'Equipment code {e.params[1]} already in use')

    def get_vessel_equipments(self, vessel_id, status):
        self._validate_vessel_id(vessel_id)
        status_enum = self._validate_status(status)
        return self._equipment_repo.get_by_vessel_and_status(vessel_id, status_enum)

    def inactivate_equipments(self, vessel_id, codes):
        self._validate_vessel_id(vessel_id)
        self._equipment_repo.update_status_by_code(vessel_id, codes, Status.INACTIVE)

    def _validate_vessel_id(self, vessel_id) -> Vessel:
        vessel = self._vessel_repo.get(vessel_id)
        if vessel is None:
            raise NotFound(f'Vessel with id {vessel_id} not found')
        return vessel

    @staticmethod
    def _validate_status(status):
        if status is None:
            return None

        try:
            status_enum = Status[status.upper()]
        except KeyError:
            raise BadRequest(f'Invalid status: {status}')
        return status_enum
