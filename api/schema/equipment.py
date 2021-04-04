from api.models.equipment import Equipment
from api.ma import ma


class EquipmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Equipment


