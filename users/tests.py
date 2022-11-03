import json

from rest_framework import status
from rest_framework.test import APITestCase


class UserRegisterAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@test.com",
            "password": "test1234",
            "nickname": "test",
            "phone": "+821012341234",
            "address": "test시 test동 test로"
        }
        self.invalid_user_data = {
            "email": "test@test.com@test.com",
            "password": "test1234",
            "nickname": "test",
            "phone": "+821012341234",
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


class UserLoginAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@test.com",
            "password": "test1234",
            "nickname": "test",
            "phone": "+821012341234",
            "address": "test시 test동 test로"
        }
        self.client.post('/register', self.user_data)

        self.login_info = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.fake_info = {
            "email": "test333@test.com",
            "password": "test1234",
        }

    def test_login(self):
        response = self.client.post('/login', self.login_info)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Token", str(response.content))

    def test_with_not_registered_account_should_return_401(self):
        response = self.client.post('/login', self.fake_info)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@test.com",
            "password": "test1234",
            "nickname": "test",
            "phone": "+821012341234",
            "address": "test시 test동 test로"
        }
        self.login_info = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.client.post('/register', self.user_data)
        self.user = self.client.post('/login', self.login_info)

    def test_logout_with_authenticated_account_should_delete_token(self):
        headers = {'HTTP_AUTHORIZATION': "token " + json.loads(self.user.content)['Token']}
        response = self.client.get('/logout', None, **headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
