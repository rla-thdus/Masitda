import json

import factory
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import FoodCategory
from users.factories import UserFactory


class RestaurantAPITest(APITestCase):
    def setUp(self):
        self.user = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.client.post('/register', self.user)
        self.login_info = {
            "email": self.user['email'],
            "password": self.user['password'],
        }
        self.login_user = self.client.post('/login', self.login_info)

    @classmethod
    def setUpTestData(cls):
        FoodCategory.objects.create(
            type = "중식"
        )

    def test_new_restaurant_should_create(self):
        headers = {'HTTP_AUTHORIZATION': "token " + json.loads(self.login_user.content)['Token']}
        restaurant_info = {
            "name": "test 식당",
            "category": "1",
            "address": "test",
            "phone": "+82111222333",
            "content": "test",
            "min_order_price": 20000,
            "delivery_price": 3000,
            "open_time": "09:00:00",
            "close_time": "22:00:00"
        }
        response = self.client.post('/restaurant', restaurant_info, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
