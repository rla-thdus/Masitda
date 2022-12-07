from rest_framework import status
from rest_framework.test import APITestCase

from orders.factories import CartFactory, CartItemFactory
from restaurants.factories import RestaurantFactory, MenuFactory
from users.factories import UserFactory


class CartAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
        self.client.force_authenticate(user=self.owner)
        self.restaurant = RestaurantFactory.create(user=self.owner)
        self.menu = MenuFactory.create(restaurant=self.restaurant)

        self.user = UserFactory.create()
        self.cart = CartFactory.create(user=self.user)
        self.cart_item = CartItemFactory.create(cart=self.cart, menu=self.menu)

        self.new_user = UserFactory.create()
        self.client.force_authenticate(user=self.new_user)


    def test_menu_add_in_cart(self):
        data = {
            'menu': self.menu.id,
            'quantity': 3
        }
        response = self.client.post(f'/carts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 3)

    def test_get_cart_should_return_200_when_exists_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/carts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_get_cart_should_return_200_when_not_exists_cart(self):
        response = self.client.get(f'/carts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'NOT_EXISTS_CART')

    def test_delete_exists_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/carts/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'DELETED')

    def test_delete_cart_item_with_exists_item(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/carts/items/{self.cart_item.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'DELETED')

    def test_delete_cart_item_with_not_exists_item_should_return_404(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/carts/items/{self.cart_item.id + 1}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'NOT_EXISTS_CART_ITEM')

    def test_delete_cart_item_with_not_exists_cart_should_return_404(self):
        response = self.client.delete(f'/carts/items/{self.cart_item.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'NOT_EXISTS_CART')

    def test_update_cart_item_quantity_should_applied(self):
        data = {"quantity": 3}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/carts/items/{self.cart_item.id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], data['quantity'])
