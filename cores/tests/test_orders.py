from rest_framework import status
from rest_framework.test import APITestCase

from cores.factories import RestaurantFactory, MenuFactory, OrderStatusFactory, CartFactory, CartItemFactory
from accounts.factories import UserFactory
from cores.models import Order


class OrderAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
        OrderStatusFactory.create(id=1)
        OrderStatusFactory.create(id=2, name='주문 취소')
        self.accept = OrderStatusFactory.create(id=3, name='주문 수락')
        self.client.force_authenticate(user=self.owner)
        self.restaurant = RestaurantFactory.create(user=self.owner, min_order_price=8000)
        self.menu = MenuFactory.create(restaurant=self.restaurant, price=4000)

        self.user = UserFactory.create()
        self.cart = CartFactory.create(user=self.user, restaurant=self.restaurant)
        self.cart_item = CartItemFactory.create(cart=self.cart, menu=self.menu, quantity=2)
        self.client.force_authenticate(user=self.user)

        self.new_user = UserFactory.create()
        self.empty_cart = CartFactory.create(user=self.new_user)


    def test_order_cart_should_be_success(self):
        response = self.client.post(f'/v1/carts/{self.cart.id}/orders')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_should_fail_with_does_not_enough_minimum_order_price(self):
        self.client.force_authenticate(user=self.new_user)
        c = CartFactory.create(user=self.new_user, restaurant=self.restaurant)
        CartItemFactory.create(cart=c, menu=self.menu, quantity=1)
        response = self.client.post(f'/v1/carts/{c.id}/orders')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Order amount less than minimum order amount')

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

    def test_get_restaurant_order_history(self):
        self.client.post(f'/v1/carts/{self.cart.id}/orders')
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f'/v1/orders')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cancel_order_before_restaurant_accept_order(self):
        order = self.client.post(f'/v1/carts/{self.cart.id}/orders')
        response = self.client.delete(f'/v1/orders/{order.data["id"]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cancel_order_already_accepted_order_should_failed(self):
        order = self.client.post(f'/v1/carts/{self.cart.id}/orders')
        accpet_order = Order.objects.get(id=order.data['id'])
        accpet_order.order_status = self.accept
        accpet_order.save()
        response = self.client.delete(f'/v1/orders/{order.data["id"]}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_order_can_not_allow_to_restaurant_owner(self):
        order = self.client.post(f'/v1/carts/{self.cart.id}/orders')
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f'/v1/orders/{order.data["id"]}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
