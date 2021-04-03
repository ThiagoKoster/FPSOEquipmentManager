import flask_unittest
import json
from api.app import create_app
from api.models.vessel_model import Vessel
from api.models.equipment_model import Equipment, Status
from api.db import db
from http import HTTPStatus


class TestEquipment(flask_unittest.AppTestCase):
    def create_app(self):
        return create_app(':memory:')

    def setUp(self, app):
        db.app = app

    def test_post_equipment_return_notFound_when_vessel_not_in_db(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = HTTPStatus.NOT_FOUND

            # ACT
            response, data = self._post_equipment(client, vessel_id=10, code='GPS0001')

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertTrue('Vessel with id 10 not found' in data['message'])

    def test_post_equipment_return_conflict_when_code_duplicated(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = HTTPStatus.CONFLICT

            vessel = Vessel(code='MV102')
            vessel.equipments = [Equipment(name='GPS', code='GPS0001', location='Brazil', vessel_id=0)]
            db.session.add(vessel)
            db.session.commit()
            # ACT
            response, data = self._post_equipment(client, vessel_id=1, code='GPS0001')

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertTrue('Equipment code GPS0001 already in use' in data['message'])

    def test_post_equipment_return_badRequest_when_wrong_requestBody(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = HTTPStatus.BAD_REQUEST

            # ACT
            response, data = self._wrong_post_equipment(client)

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data['message'], 'Input payload validation failed')

    def test_get_equipment_return_NOT_FOUND_when_vessel_not_in_db(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = HTTPStatus.NOT_FOUND

            # ACT
            response, data = self._get_equipments(client, 1)

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data['message'], 'Vessel with id 1 not found')

    def test_get_equipment_return_active_equipments(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = HTTPStatus.OK
            expected_response = [{'id': 1, 'name': 'GPS', 'code': 'GPS0001', 'location': 'Brazil', 'status': 'ACTIVE'}]
            expected_response2 = [{'id': 3, 'name': 'GPS', 'code': 'GPS0003', 'location': 'Brazil', 'status': 'ACTIVE'}]

            vessel = Vessel(code='MV102')
            active_equipment = Equipment(name='GPS', code='GPS0001', location='Brazil', vessel_id=0)
            deactivated_equipment = Equipment(name='GPS', code='GPS0002', location='Brazil', vessel_id=0)
            deactivated_equipment.status = Status.INACTIVE
            vessel.equipments = [active_equipment, deactivated_equipment]

            vessel2 = Vessel(code='MV103')
            vessel2.equipments = [Equipment(name='GPS', code='GPS0003', location='Brazil', vessel_id=0)]
            db.session.add(vessel)
            db.session.add(vessel2)
            db.session.commit()

            # ACT
            response, data = self._get_equipments_with_status(client, 1, 'ACTIVE')
            response2, data2 = self._get_equipments_with_status(client, 2, 'ACTIVE')

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data, expected_response)
            self.assertEqual(response2.status_code, expected_status_code)
            self.assertEqual(data2, expected_response2)

    def test_get_equipment_return_badRequest_when_wrong_status(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = HTTPStatus.BAD_REQUEST

            vessel = Vessel(code='MV102')
            vessel.equipments = [Equipment(name='GPS', code='GPS0001', location='Brazil', vessel_id=0)]
            db.session.add(vessel)
            db.session.commit()

            # ACT
            response, data = self._get_equipments_with_status(client, 1, 'WRONG_STATUS')

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data['message'], 'Invalid status: WRONG_STATUS')

    def test_patch_equipment_return_badRequest_when_invalid_body(self, app):
        with app.test_client() as client:
            # ARRANGE

            expected_status_code = HTTPStatus.BAD_REQUEST
            request_body = [{'code': 'GPS1'}, {'wrong_prop': 'GPS2'}]

            # ACT
            response, data = self._inactivate_equipments(client, 1, request_body)

            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data['message']['1']['wrong_prop'][0], 'Unknown field.')

    def test_patch_equipment_return_noContent_when_inactivate(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = HTTPStatus.NO_CONTENT
            request_body = [{'code': 'GPS1'}, {'code': 'GPS2'}]
            vessel = Vessel(code='MV102')
            eq1 = Equipment(name='GPS', code='GPS1', location='Brazil', vessel_id=0)
            eq2 = Equipment(name='GPS', code='GPS2', location='Brazil', vessel_id=0)
            eq3 = Equipment(name='GPS', code='GPS3', location='Brazil', vessel_id=0)
            vessel.equipments = [eq1, eq2, eq3]
            vessel2 = Vessel(code='MV103')
            vessel2.equipments = [Equipment(name='GPS', code='GPS4', location='Brazil', vessel_id=0)]

            db.session.add(vessel)
            db.session.add(vessel2)
            db.session.commit()

            response, data = self._inactivate_equipments(client, 1, request_body)

            inactive_equipments = [eq for eq in vessel.equipments if eq.status == Status.INACTIVE]

            self.assertEqual(response.status_code, expected_status_code)
            self.assertIsNone(data)
            self.assertNotIn(eq3, inactive_equipments)
            self.assertEqual([eq1, eq2], inactive_equipments)

    @staticmethod
    def _inactivate_equipments(client, vessel_id, request_body):
        response = client.patch(
            f'/vessels/{vessel_id}/equipments',
            content_type='application/json',
            data=json.dumps(request_body),
            follow_redirects=True
        )
        data = None
        if response.status_code != HTTPStatus.NO_CONTENT:
            data = json.loads(response.data.decode())

        return response, data

    @staticmethod
    def _get_equipments_with_status(client, vessel_id, status):
        response = client.get(
            f'/vessels/{vessel_id}/equipments?status={status}',
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        return response, data

    @staticmethod
    def _get_equipments(client, vessel_id):
        response = client.get(
            f'/vessels/{vessel_id}/equipments',
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        return response, data

    @staticmethod
    def _post_equipment(client, vessel_id, code):
        response = client.post(
            f'/vessels/{vessel_id}/equipments',
            data=json.dumps(dict(
                name='GPS',
                code=code,
                location='Brazil'
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        return response, data

    @staticmethod
    def _wrong_post_equipment(client):
        response = client.post(
            f'/vessels/1/equipments',
            data=json.dumps(dict(
                name2='GPS',
                code3='GPS001',
                location4='Brazil'
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        return response, data
