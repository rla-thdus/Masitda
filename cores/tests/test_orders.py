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


    def test_order_cart_should_be_success(self):
        response = self.client.post(f'/v1/carts/{self.cart.id}/orders')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_order_detail(self):
        order = self.client.post(f'/v1/carts/{self.cart.id}/orders')
        response = self.client.get(f'/v1/orders/{order.data["id"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('total_price' in response.data)
        self.assertTrue('delivery_price' in response.data)
        self.assertTrue('amount_payment' in response.data)
