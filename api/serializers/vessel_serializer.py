from api.restx import restX_api
from flask_restx import fields

vessel_serializer = restX_api.model('Vessel', {
    'id': fields.Integer(readonly=True),
    'code': fields.String(required=True, description='The vessel\'s code')
})
