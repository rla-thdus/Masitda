import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from cores.factories import RestaurantFactory, MenuFactory, OrderStatusFactory, CartFactory, CartItemFactory, \
    OrderFactory, ReviewFactory
from accounts.factories import UserFactory


class ReviewAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
        self.owner2 = UserFactory.create(role='사장')
        OrderStatusFactory.create(id=1)
        self.accept = OrderStatusFactory.create(id=2, name='주문 수락')
        self.deny = OrderStatusFactory.create(id=3, name='주문 거절')
        self.client.force_authenticate(user=self.owner)
        self.restaurant = RestaurantFactory.create(user=self.owner, min_order_price=8000)
        self.restaurant2 = RestaurantFactory.create(user=self.owner2, min_order_price=8000)
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
        self.review = ReviewFactory(order=self.order)
        self.client.force_authenticate(user=self.owner)

    def test_add_review_comment_success(self):
        response = self.client.post(f'/v1/reviews/{self.review.id}/comments', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_review_comment_should_fail_with_not_exists_review(self):
        response = self.client.post(f'/v1/reviews/{self.review.id + 1}/comments', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
