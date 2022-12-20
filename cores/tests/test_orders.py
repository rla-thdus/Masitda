from rest_framework import status
from rest_framework.test import APITestCase

from cores.factories import RestaurantFactory, MenuFactory, OrderStatusFactory, CartFactory, CartItemFactory
from accounts.factories import UserFactory


class OrderAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
        OrderStatusFactory.create(id=1)
        self.client.force_authenticate(user=self.owner)
        self.restaurant = RestaurantFactory.create(user=self.owner)
        self.menu = MenuFactory.create(restaurant=self.restaurant)

        self.user = UserFactory.create()
        self.cart = CartFactory.create(user=self.user, restaurant=self.restaurant)
        self.cart_item = CartItemFactory.create(cart=self.cart, menu=self.menu)
        self.client.force_authenticate(user=self.user)

        self.new_user = UserFactory.create()
        self.empty_cart = CartFactory.create(user=self.new_user)


    def test_order_cart_should_be_success(self):
        response = self.client.post(f'/v1/carts/{self.cart.id}/orders')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_cart_should_failed_with_empty_cart(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f'/v1/carts/{self.empty_cart.id}/orders')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_detail(self):
        order = self.client.post(f'/v1/carts/{self.cart.id}/orders')
        response = self.client.get(f'/v1/orders/{order.data["id"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('total_price' in response.data)
        self.assertTrue('delivery_price' in response.data)
        self.assertTrue('amount_payment' in response.data)

    def test_get_my_order_history(self):
        self.client.post(f'/v1/carts/{self.cart.id}/orders')
        response = self.client.get(f'/v1/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
