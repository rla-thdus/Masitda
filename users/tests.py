from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationAPIViewTest(APITestCase):
    def test_registration(self):
        user_data = {
            "email": "test@test.com",
            "password": "test1234",
            "nickname": "test",
            "address": "test시 test동 test로"
        }

        response = self.client.post('/register', user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_same_user_register_should_return_400(self):
        user_data = {
            "email": "test@test.com",
            "password": "test1234",
            "nickname": "test",
            "address": "test시 test동 test로"
        }

        self.client.post('/register', user_data)
        response = self.client.post('/register', user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
