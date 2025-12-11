import unittest
import json
from app import app

class ElementsAPITest(unittest.TestCase):

    def setUp(self):
        # Set up a test client
        self.app = app.test_client()
        self.app.testing = True

        # Get a JWT token for all protected routes
        login_payload = {
            "username": "USER",
            "password": "USER123"
        }
        response = self.app.post('/login',
                                 data=json.dumps(login_payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.token = json.loads(response.data.decode())['token']
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    # TEST: GET ALL
    def test_get_all_elements(self):
        response = self.app.get('/api/elements', headers=self.headers)
        self.assertEqual(response.status_code, 200)

    # TEST: CREATE
    def test_create_element(self):
        payload = {
            "element": "TestElement",
            "element_state": "Testing"
        }
        response = self.app.post('/api/elements',
                                 data=json.dumps(payload),
                                 headers=self.headers)

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data.decode())
        self.created_id = data['element_id']

    # TEST: UPDATE
    def test_update_element(self):
        # First create an element
        payload = {
            "element": "Temporary",
            "element_state": "TempState"
        }
        create_res = self.app.post('/api/elements',
                                   data=json.dumps(payload),
                                   headers=self.headers)
        created_id = json.loads(create_res.data.decode())['element_id']

        # Now update it
        update_payload = {
            "element": "Updated",
            "element_state": "UpdatedState"
        }
        response = self.app.put(f'/api/elements/{created_id}',
                                data=json.dumps(update_payload),
                                headers=self.headers)

        self.assertEqual(response.status_code, 200)

    # TEST: DELETE
    def test_delete_element(self):
        # Create first
        payload = {
            "element": "DeleteMe",
            "element_state": "ToBeDeleted"
        }
        create_res = self.app.post('/api/elements',
                                   data=json.dumps(payload),
                                   headers=self.headers)
        created_id = json.loads(create_res.data.decode())['element_id']

        # Now delete
        response = self.app.delete(f'/api/elements/{created_id}',
                                   headers=self.headers)

        self.assertEqual(response.status_code, 200)

    # TEST: INVALID INPUT
    def test_invalid_post(self):
        payload = {
            "element": ""
        }  # Missing element_state
        response = self.app.post('/api/elements',
                                 data=json.dumps(payload),
                                 headers=self.headers)

        self.assertEqual(response.status_code, 400)

    # TEST: WITHOUT TOKEN 
    def test_no_token(self):
        response = self.app.get('/api/elements')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
