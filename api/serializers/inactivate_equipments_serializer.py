from api.restx import restX_api
from flask_restx import fields
import marshmallow

inactivate_equipment_serializer = restX_api.model('InactivateEquipment', {
    'code': fields.String(required=True, description='The equipment\'s code'),
})


class InactivateEquipmentSchema(marshmallow.Schema):
    code = marshmallow.fields.Str()



