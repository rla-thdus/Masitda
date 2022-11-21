import json

import factory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from restaurants.models import FoodCategory
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
        self.headers = {'HTTP_AUTHORIZATION': "token " + json.loads(self.login_owner.content)['Token']}

    @classmethod
    def setUpTestData(cls):
        FoodCategory.objects.create(
            id=1, type = "중식"
        )
        cls.restaurant_info = {
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

    def test_new_restaurant_should_create(self):
        response = self.client.post('/restaurants/', self.restaurant_info, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_should_not_access_create_restaurant_api(self):
        headers = {'HTTP_AUTHORIZATION': "token " + json.loads(self.login_user.content)['Token']}
        response = self.client.post('/restaurants/', {}, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_create_restaurant_user_should_return_empty_object(self):
        response = self.client.get('/restaurants/', None, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode(), '[]')


class RestaurantDetailAPITest(APITestCase):
    headers = ''
    @classmethod
    def setUpClass(cls):
        super(RestaurantDetailAPITest, cls).setUpClass()
        client = APIClient()
        owner = factory.build(dict, FACTORY_CLASS=UserFactory, role='사장')
        client.post('/register', owner)
        owner_login_info = {
            "email": owner['email'],
            "password": owner['password'],
        }
        login_owner = client.post('/login', owner_login_info)
        cls.headers = {'HTTP_AUTHORIZATION': "token " + json.loads(login_owner.content)['Token']}
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
        res = client.post('/restaurants/', restaurant_info, **cls.headers)
        cls.restaurant_pk = json.dumps(res.data.get('id'))

    @classmethod
    def setUpTestData(cls):
        FoodCategory.objects.create(
            id=1, type="중식"
        )

    def test_does_not_exist_restaurant_pk_should_return_404(self):
        does_not_exist_restaurant_pk = int(self.restaurant_pk) + 1
        response = self.client.get(f'/restaurants/{does_not_exist_restaurant_pk}', None, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_specific_restaurant_should_return_with_menu_set(self):
        response = self.client.get(f'/restaurants/{self.restaurant_pk}', None, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('menu_set' in response.content.decode())


class MenuAPITest(APITestCase):
    headers = ''
    @classmethod
    def setUpClass(cls):
        super(MenuAPITest, cls).setUpClass()
        client = APIClient()
        owner = factory.build(dict, FACTORY_CLASS=UserFactory, role='사장')
        client.post('/register', owner)
        owner_login_info = {
            "email": owner['email'],
            "password": owner['password'],
        }
        login_owner = client.post('/login', owner_login_info)
        cls.headers = {'HTTP_AUTHORIZATION': "token " + json.loads(login_owner.content)['Token']}
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
        client.post('/restaurants/', restaurant_info, **cls.headers)
        data = {
            "name": "메뉴 이름",
            "price": 20000,
            "description": "메뉴 설명"
        }
        client.post('/restaurants/1/menus', data, **cls.headers)

    @classmethod
    def setUpTestData(cls):
        FoodCategory.objects.create(
            type="중식"
        )

    def test_add_menu_should_success_with_name_price_exists(self):
        data = {
            "name": "메뉴 이름",
            "price": 20000,
            "description": "메뉴 설명"
        }
        response = self.client.post('/restaurants/1/menus', data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_menu_should_fail_with_invalid_data(self):
        data = {
            "price": 20000,
            "description": "메뉴 설명"
        }
        response = self.client.post('/restaurants/1/menus', data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_menu_should_fail_with_does_not_create_restaurant(self):
        data = {
            "name": "메뉴 이름",
            "price": 20000,
            "description": "메뉴 설명"
        }
        response = self.client.post('/restaurants/2/menus', data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_menu_should_success(self):
        data = {
            "name": "업데이트",
            "price": 30000,
            "description": "메뉴 설명"
        }
        response = self.client.patch('/restaurants/1/menus/1', data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('업데이트' in response.content.decode())

    def test_update_menu_should_fail_with_not_exists_menu_pk(self):
        data = {
            "name": "업데이트",
            "price": 30000,
            "description": "메뉴 설명"
        }
        response = self.client.patch('/restaurants/1/menus/4', data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_menu_should_fail_not_exists_menu_pk(self):
        response = self.client.delete('/restaurants/1/menus/4', None, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_menu_should_success(self):
        response = self.client.delete('/restaurants/1/menus/1', None, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
