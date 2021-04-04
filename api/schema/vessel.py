from api.models.vessel import Vessel
from api.ma import ma


class VesselSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vessel


