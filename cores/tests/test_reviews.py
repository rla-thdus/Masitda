import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from cores.factories import RestaurantFactory, MenuFactory, OrderStatusFactory, CartFactory, CartItemFactory, \
    OrderFactory
from accounts.factories import UserFactory
from cores.models import Order


class ReviewAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
        OrderStatusFactory.create(id=1)
        self.accept = OrderStatusFactory.create(id=2, name='주문 수락')
        OrderStatusFactory.create(id=3, name='주문 거절')
        self.client.force_authenticate(user=self.owner)
        self.restaurant = RestaurantFactory.create(user=self.owner, min_order_price=8000)
        self.menu = MenuFactory.create(restaurant=self.restaurant, price=4000)

        self.user = UserFactory.create()
        self.cart = CartFactory.create(user=self.user, restaurant=self.restaurant)
        self.cart.ordered_at = datetime.datetime.now(datetime.timezone.utc)
        self.cart.save()
        self.cart_item = CartItemFactory.create(cart=self.cart, menu=self.menu, quantity=2)
        self.client.force_authenticate(user=self.user)

        self.new_user = UserFactory.create()
        self.order = OrderFactory(cart=self.cart, order_status=self.accept)
        self.data = {
            "text": "good"
        }

    def test_review_order_success(self):
        response = self.client.post(f'/v1/orders/{self.order.id}/reviews', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_should_fail_with_not_own_order(self):
        self.client.force_authenticate(user=self.new_user)
        response = self.client.post(f'/v1/orders/{self.order.id}/reviews', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
