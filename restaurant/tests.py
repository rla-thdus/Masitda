import json

import factory
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import FoodCategory
from users.factories import UserFactory


class RestaurantAPITest(APITestCase):
    def setUp(self):
        self.user = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.owner = factory.build(dict, FACTORY_CLASS=UserFactory, role='사장')
        self.client.post('/register', self.user)
        self.client.post('/register', self.owner)
        self.user_login_info = {
            "email": self.user['email'],
            "password": self.user['password'],
        }
        self.owner_login_info = {
            "email": self.owner['email'],
            "password": self.owner['password'],
        }
        self.login_user = self.client.post('/login', self.user_login_info)
        self.login_owner = self.client.post('/login', self.owner_login_info)

    @classmethod
    def setUpTestData(cls):
        FoodCategory.objects.create(
            type = "중식"
        )

    def test_new_restaurant_should_create(self):
        headers = {'HTTP_AUTHORIZATION': "token " + json.loads(self.login_owner.content)['Token']}
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

    def test_normal_user_should_not_access_create_restaurant_api(self):
        headers = {'HTTP_AUTHORIZATION': "token " + json.loads(self.login_user.content)['Token']}
        response = self.client.post('/restaurant', {}, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
