import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from cores.factories import RestaurantFactory, MenuFactory, OrderStatusFactory, CartFactory, CartItemFactory, \
    OrderFactory, ReviewFactory, CommentFactory
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

    def test_add_review_comment_should_fail_with_not_own_restaurant_review(self):
        self.client.force_authenticate(user=self.owner2)
        response = self.client.post(f'/v1/reviews/{self.review.id}/comments', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_review_comment_should_fail_with_not_enough_data(self):
        response = self.client.post(f'/v1/reviews/{self.review.id}/comments')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_review_comment_should_success(self):
        comment = CommentFactory(review=self.review)
        response = self.client.delete(f'/v1/reviews/{self.review.id}/comments/{comment.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_review_comment_should_fail_with_not_exists_comment(self):
        comment = CommentFactory(review=self.review)
        response = self.client.delete(f'/v1/reviews/{self.review.id}/comments/{comment.id + 1}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
