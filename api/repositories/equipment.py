from flask_sqlalchemy import SQLAlchemy

from api.models.equipment import Equipment, Status


class EquipmentRepository:
    def __init__(self, db: SQLAlchemy):
        self._db = db

    def add(self, equipment_list) -> Equipment:
        for e in equipment_list:
            self._db.session.add(e)
        self._db.session.commit()
        return equipment_list

    def update_status_by_code(self, vessel_id: int, codes: [str], status: Status):
        Equipment.query.filter_by(vessel_id=vessel_id) \
            .filter(Equipment.code.in_(codes)) \
            .update(dict(status=status))
        self._db.session.commit()

    @staticmethod
    def get_by_vessel_and_status(vessel_id: int, status: Status) -> [Equipment]:
        if status is None:
            return Equipment.query.filter(Equipment.vessel_id == vessel_id).all()
        return Equipment.query.filter(Equipment.vessel_id == vessel_id, Equipment.status == status).all()
