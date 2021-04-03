from api.restx import restX_api
from flask_restx import fields
from api.models.equipment_model import Status


equipment_serializer = restX_api.model('Equipment', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True, description='The equipment\'s name'),
    'code': fields.String(required=True, description='The equipment\'s code'),
    'location': fields.String(required=True, description='The equipment\'s location'),
    'status': fields.String(readonly=True, description=' The equipment\'s status',
                            enum=[x.value for x in Status], attribute='status.name')
})
