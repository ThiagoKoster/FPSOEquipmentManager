import flask_unittest
import json
from api.app import create_app


class TestVessel(flask_unittest.AppTestCase):
    def create_app(self):
        return create_app(':memory:')

    def test_post_return_created_vessel_when_no_problems(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_code = 'MV102'
            expected_id = 1
            expected_status_code = 201
            # ACT
            response, data = self.post_vessel(client, expected_code)

            # ASSERT
            assert response.status_code == expected_status_code
            assert data['id'] == expected_id
            assert data['code'] == expected_code

    def test_post_return_conflict_when_duplicate_vessel_code(self, app):
        with app.test_client() as client:
            # ARRANGE
            code = 'MV101'
            expected_status_code = 409

            # ACT
            self.post_vessel(client, code)
            response, data = self.post_vessel(client, code)

            # ASSERT
            assert response.status_code == expected_status_code
            assert data['message'] == 'Vessel Code already exists in database'

    def test_post_return_bad_request_when_code_is_blank(self, app):
        with app.test_client() as client:
            # ARRANGE
            expected_status_code = 400

            # ACT
            response, data = self.wrong_post(client)

            #ASSERT
            assert response.status_code == expected_status_code
            assert data['message'] == 'Input payload validation failed'

    @staticmethod
    def post_vessel(client, code):
        response = client.post(
            '/vessel',
            data=json.dumps(dict(
                code=code
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        return response, data

    @staticmethod
    def wrong_post(client):
        response = client.post(
            '/vessel',
            data=json.dumps(dict(
                wrong_property='test'
            )),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.data.decode())
        return response, data
