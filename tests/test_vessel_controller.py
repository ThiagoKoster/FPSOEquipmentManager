import flask_unittest
import json
from api.app import create_app
from api.models.vessel_model import Vessel
from api.models.equipment_model import Equipment
from api.db import db


class TestVessel(flask_unittest.AppTestCase):
    def create_app(self):
        return create_app(':memory:')

    def test_post_return_created_vessel_when_no_problems(self, app):
        with app.test_client() as client:
            # ARRANGE

            expected_response = {'id': 1, 'code': 'MV012'}
            expected_status_code = 201
            # ACT
            response, data = self.post_vessel(client, expected_response['code'])
            vessel = Vessel.query.get(1)

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data, expected_response)
            self.assertEqual(expected_response['id'], vessel.id)
            self.assertEqual(expected_response['code'], vessel.code)
            self.assertEqual([], vessel.equipments)

    def test_post_return_conflict_when_duplicate_vessel_code(self, app):
        with app.test_client() as client:
            # ARRANGE
            code = 'MV101'
            expected_status_code = 409

            # ACT
            self.post_vessel(client, code)
            response, data = self.post_vessel(client, code)

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data['message'], 'Vessel Code already exists in database')

    def test_post_return_bad_request_when_code_is_blank(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = 400

            # ACT
            response, data = self._wrong_post_vessel(client)

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data['message'], 'Input payload validation failed')

    def test_post_equipment_return_notFound_when_vessel_not_in_db(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = 404

            # ACT
            response, data = self._post_equipment(client, vessel_id=1, code='GPS0001')

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertTrue('Vessel with id 1 not found' in data['message'])

    def test_post_equipment_return_conflict_when_code_duplicated(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = 409
            db.app = app
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
            expected_status_code = 400

            # ACT
            response, data = self._wrong_post_vessel(client)

            # ASSERT
            self.assertEqual(response.status_code, expected_status_code)
            self.assertEqual(data['message'], 'Input payload validation failed')

    @staticmethod
    def post_vessel(client, code):
        response = client.post(
            '/vessels',
            data=json.dumps(dict(
                code=code
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        return response, data

    @staticmethod
    def _wrong_post_vessel(client):
        response = client.post(
            '/vessels',
            data=json.dumps(dict(
                wrong_property='test'
            )),
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
    def _wrong_post_equipment(client, vessel_id, code):
        response = client.post(
            f'/vessels/{vessel_id}/equipments',
            data=json.dumps(dict(
                name2='GPS',
                code3=code,
                location4='Brazil'
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        return response, data
