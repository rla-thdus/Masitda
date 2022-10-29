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
