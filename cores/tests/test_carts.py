from rest_framework import status
from rest_framework.test import APITestCase

from cores.factories import RestaurantFactory, MenuFactory, OrderStatusFactory, CartFactory, CartItemFactory
from accounts.factories import UserFactory


class CartAPITest(APITestCase):
    def setUp(self):
        OrderStatusFactory.create(id=1)
        self.owner = UserFactory.create(role='사장')
        self.owner2 = UserFactory.create(role='사장')
        self.client.force_authenticate(user=self.owner2)
        self.restaurant2 = RestaurantFactory.create(user=self.owner2)
        self.other_restaurant_menu = MenuFactory.create(restaurant=self.restaurant2)

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
        response = self.client.post(f'/v1/carts', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 3)

    def test_add_item_should_failed_with_different_restaurant_menu(self):
        data = {
            'menu': self.menu.id,
            'quantity': 3
        }
        self.client.post(f'/v1/carts', data)
        data = {'menu': self.other_restaurant_menu.id}
        response = self.client.post(f'/v1/carts', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_cart_should_return_200_when_exists_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/v1/carts/{self.cart.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_get_cart_should_return_200_when_not_exists_cart(self):
        response = self.client.get(f'/v1/carts/{self.cart.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'NOT_EXISTS_CART')

    def test_delete_exists_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/v1/carts/{self.cart.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'DELETED')

    def test_delete_cart_item_with_exists_item(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/v1/carts/items/{self.cart_item.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'DELETED')

    def test_delete_cart_item_with_not_exists_item_should_return_404(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/v1/carts/items/{self.cart_item.id + 1}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'NOT_EXISTS_CART_ITEM')

    def test_delete_cart_item_with_not_exists_cart_should_return_404(self):
        response = self.client.delete(f'/v1/carts/items/{self.cart_item.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'NOT_EXISTS_CART')

    def test_update_cart_item_quantity_should_applied(self):
        data = {"quantity": 3}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/v1/carts/items/{self.cart_item.id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], data['quantity'])

    def test_update_cart_item_quantity_value_smaller_than_1_should_failed(self):
        data = {"quantity": 0}
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'/v1/carts/items/{self.cart_item.id}', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['quantity'], ['Ensure this value is greater than or equal to 1.'])
