from rest_framework import status
from rest_framework.test import APITestCase


class UserAccountAPIViewTest(APITestCase):
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
        self.login_info = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.fake_info = {
            "email": "test3@test.com",
            "password": "test1234",
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

    def test_login(self):
        self.client.post('/register', self.user_data)
        response = self.client.post('/login', self.login_info)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_with_not_authorized_account_should_return_401(self):
        response = self.client.post('/login', self.login_info)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)