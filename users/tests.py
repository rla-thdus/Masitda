import json

import factory
from rest_framework import status
from rest_framework.test import APITestCase

from users.factories import UserFactory


class UserRegisterAPITest(APITestCase):
    def setUp(self):
        self.user = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.invalid_user = factory.build(dict, FACTORY_CLASS=UserFactory, email="test@test@test.com")

    def test_registration(self):
        response = self.client.post('/register', self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_same_user_register_should_return_400(self):
        self.client.post('/register', self.user)
        response = self.client.post('/register', self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data_should_return_400(self):
        response = self.client.post('/register', self.invalid_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPITest(APITestCase):
    def setUp(self):
        self.user = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.client.post('/register', self.user)

        self.login_info = {
            "email": self.user.get('email'),
            "password": self.user.get('password'),
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
        self.user = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.client.post('/register', self.user)
        self.login_info = {
            "email": self.user.get('email'),
            "password": self.user.get('password'),
        }
        self.login_user = self.client.post('/login', self.login_info)

    def test_logout_with_authenticated_account_should_delete_token(self):
        headers = {'HTTP_AUTHORIZATION': "token " + json.loads(self.login_user.content)['Token']}
        response = self.client.get('/logout', None, **headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
