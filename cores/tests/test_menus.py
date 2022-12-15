from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import UserFactory
from cores.factories import RestaurantFactory, MenuFactory


class MenuAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
        self.restaurant = RestaurantFactory.create(user=self.owner)
        self.client.force_authenticate(user=self.owner)
        self.menu = MenuFactory.create(restaurant=self.restaurant)

    def test_add_menu_should_success_with_name_price_exists(self):
        data = {
            "name": "메뉴 이름",
            "price": 20000,
            "description": "메뉴 설명"
        }
        response = self.client.post(f'/v1/restaurants/{self.restaurant.id}/menus', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_menu_should_fail_with_invalid_data(self):
        data = {
            "price": 20000,
            "description": "메뉴 설명"
        }
        response = self.client.post(f'/v1/restaurants/{self.restaurant.id}/menus', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_menu_should_fail_with_does_not_create_restaurant(self):
        data = {
            "name": "메뉴 이름",
            "price": 20000,
            "description": "메뉴 설명"
        }
        response = self.client.post(f'/v1/restaurants/{self.restaurant.id + 1}/menus', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_menu_should_success(self):
        data = {
            "name": "업데이트",
            "price": 30000,
            "description": "메뉴 설명"
        }
        response = self.client.patch(f'/v1/restaurants/{self.restaurant.id}/menus/{self.menu.id}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('업데이트' in response.content.decode())

    def test_update_menu_should_fail_with_not_exists_menu_pk(self):
        data = {
            "name": "업데이트",
            "price": 30000,
            "description": "메뉴 설명"
        }
        response = self.client.patch(f'/v1/restaurants/{self.restaurant.id}/menus/{self.menu.id + 1}', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_menu_should_fail_not_exists_menu_pk(self):
        response = self.client.delete(f'/v1/restaurants/{self.restaurant.id}/menus/{self.menu.id + 1}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_menu_should_success(self):
        response = self.client.delete(f'/v1/restaurants/{self.restaurant.id}/menus/{self.menu.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
