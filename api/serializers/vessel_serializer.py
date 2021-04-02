from api.restx import api
from flask_restx import fields

vessel_serializer = api.model('Vessel', {
    'id': fields.Integer(readonly=True),
    'code': fields.String(required=True, description='The vessel\'s code')
})
