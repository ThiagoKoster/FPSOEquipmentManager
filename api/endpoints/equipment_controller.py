from flask_restx import Resource, reqparse
from flask import request
from api.restx import restX_api
from api.serializers.equipment_serializer import equipment_serializer
from api.business.equipment_business import EquipmentBus
from api.db import db
ns_equipment = restX_api.namespace('vessels')


@ns_equipment.route('/<vessel_id>/equipments')
class VesselEquipmentController(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super(VesselEquipmentController, self).__init__(api, args, kwargs)
        self.bus = EquipmentBus(db)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', required=True, type=str, help='Equipment Name cannot be blank.')
        self.parser.add_argument('code', required=True, type=str, help='Equipment Code cannot be blank.')
        self.parser.add_argument('location', required=True, type=str, help='Equipment Location cannot be blank.')

    @restX_api.expect(equipment_serializer)
    @restX_api.marshal_with(equipment_serializer, code=201)
    @restX_api.response(400, 'Bad request')
    @restX_api.response(404, 'Vessel not found')
    @restX_api.response(409, 'Equipment code already in use')
    def post(self, vessel_id):
        parse_result = self.parser.parse_args()
        new_equipment = self.bus.add_equipment(vessel_id, parse_result)

        return new_equipment, 201

    @restX_api.marshal_list_with(equipment_serializer, code=200)
    @restX_api.doc(params={'status': 'Equipment status'})
    @restX_api.response(404, 'Vessel not found')
    def get(self,  vessel_id):
        status = request.args.get('status', None)
        equipments = self.bus.get_vessel_equipments(vessel_id, status)
        return equipments, 200


