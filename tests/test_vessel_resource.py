import flask_unittest
import json
from api.app import create_app
from api.models.vessel import Vessel
from api.db import db


class TestVessel(flask_unittest.AppTestCase):
    def create_app(self):
        return create_app(':memory:')

    def setUp(self, app):
        db.app = app

    def test_post_return_created_vessel_when_no_problems(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_response = {'id': 1, 'code': 'MV012', 'equipments': []}
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
            self.assertEqual(data['message']['code'], ['Missing data for required field.'])
            self.assertEqual(data['message']['wrong_property'], ['Unknown field.'])

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

