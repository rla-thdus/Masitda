import json

import factory
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from restaurants.models import FoodCategory
from users.factories import UserFactory


class RestaurantAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.owner = UserFactory.create(role='사장')
        self.client.force_authenticate(user=self.owner)

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
        response = self.client.post('/restaurants/', self.restaurant_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_should_not_access_create_restaurant_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/restaurants/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_restaurants_should_return_list(self):
        response = self.client.get('/restaurants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class RestaurantDetailAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
        self.other_owner = UserFactory.create(role='사장')
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
        self.client.force_authenticate(user=self.owner)
        res = self.client.post('/restaurants/', restaurant_info)
        self.restaurant_pk = json.dumps(res.data.get('id'))

    @classmethod
    def setUpTestData(cls):
        FoodCategory.objects.create(
            id=1, type="중식"
        )

    def test_does_not_exist_restaurant_pk_should_return_404(self):
        does_not_exist_restaurant_pk = int(self.restaurant_pk) + 1
        response = self.client.get(f'/restaurants/{does_not_exist_restaurant_pk}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_specific_restaurant_should_return_with_menu_set(self):
        response = self.client.get(f'/restaurants/{self.restaurant_pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('menu_set' in response.content.decode())

    def test_update_restaurant_only_can_owner(self):
        update_data = {"name": "change name success"}
        response = self.client.patch(f'/restaurants/{self.restaurant_pk}', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_update_restaurant_if_not_owner_should_permission_fail(self):
        self.client.force_authenticate(user=self.other_owner)
        update_data = {"name": "change name success"}
        response = self.client.patch(f'/restaurants/{self.restaurant_pk}', update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MenuAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
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
        self.client.force_authenticate(user=self.owner)
        res = self.client.post('/restaurants/', restaurant_info)
        self.restaurant_pk = json.dumps(res.data.get('id'))
        data = {
            "name": "메뉴 이름",
            "price": 20000,
            "description": "메뉴 설명"
        }
        res = self.client.post(f'/restaurants/{self.restaurant_pk}/menus', data)
        self.menu_pk = json.dumps(res.data.get('id'))

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
        response = self.client.post(f'/restaurants/{self.restaurant_pk}/menus', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_menu_should_fail_with_invalid_data(self):
        data = {
            "price": 20000,
            "description": "메뉴 설명"
        }
        response = self.client.post(f'/restaurants/{self.restaurant_pk}/menus', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_menu_should_fail_with_does_not_create_restaurant(self):
        data = {
            "name": "메뉴 이름",
            "price": 20000,
            "description": "메뉴 설명"
        }
        response = self.client.post(f'/restaurants/{int(self.restaurant_pk) + 1}/menus', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_menu_should_success(self):
        data = {
            "name": "업데이트",
            "price": 30000,
            "description": "메뉴 설명"
        }
        response = self.client.patch(f'/restaurants/{self.restaurant_pk}/menus/{self.menu_pk}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('업데이트' in response.content.decode())

    def test_update_menu_should_fail_with_not_exists_menu_pk(self):
        data = {
            "name": "업데이트",
            "price": 30000,
            "description": "메뉴 설명"
        }
        response = self.client.patch(f'/restaurants/{self.restaurant_pk}/menus/{int(self.menu_pk) + 1}', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_menu_should_fail_not_exists_menu_pk(self):
        response = self.client.delete(f'/restaurants/{self.restaurant_pk}/menus/{int(self.menu_pk) + 1}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_menu_should_success(self):
        response = self.client.delete(f'/restaurants/{self.restaurant_pk}/menus/{self.menu_pk}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
