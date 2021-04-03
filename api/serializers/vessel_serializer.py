from api.restx import restX_api
from flask_restx import fields
from api.serializers.equipment_serializer import equipment_serializer

vessel_serializer = restX_api.model('Vessel', {
    'id': fields.Integer(readonly=True),
    'code': fields.String(required=True, description='The vessel\'s code'),
    'equipments': fields.List(fields.Nested(equipment_serializer), readonly=True)
})
