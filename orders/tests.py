from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.factories import RestaurantFactory, MenuFactory
from users.factories import UserFactory


class CartAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.owner = UserFactory.create(role='사장')
        self.client.force_authenticate(user=self.owner)
        self.restaurant = RestaurantFactory.create(user=self.owner)
        self.menu = MenuFactory.create(restaurant=self.restaurant)
        self.client.force_authenticate(user=self.user)

    def test_menu_add_in_cart(self):
        data = {
            'menu': self.menu.id,
            'quantity': 3
        }
        response = self.client.post(f'/carts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 3)

    def test_get_cart_should_return_200_when_exists_cart(self):
        data = {
            'menu': self.menu.id,
            'quantity': 3
        }
        self.client.post(f'/carts/', data)
        response = self.client.get(f'/carts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_get_cart_should_return_200_when_not_exists_cart(self):
        response = self.client.get(f'/carts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'NOT_EXISTS_CART')

    def test_delete_exists_cart(self):
        data = {
            'menu': self.menu.id,
            'quantity': 3
        }
        self.client.post(f'/carts/', data)
        response = self.client.delete(f'/carts/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'DELETED')
