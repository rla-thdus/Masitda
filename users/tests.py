from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationAPIViewTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@test.com",
            "password": "test1234",
            "nickname": "test",
            "address": "test시 test동 test로"
        }
        self.invalid_user_data = {
            "email": "test@test.com@test.com",
            "password": "test1234",
            "nickname": "test",
            "address": "test시 test동 test로"
        }

    def test_registration(self):
        response = self.client.post('/register', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_same_user_register_should_return_400(self):
        self.client.post('/register', self.user_data)
        response = self.client.post('/register', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data_should_return_400(self):
        response = self.client.post('/register', self.invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
