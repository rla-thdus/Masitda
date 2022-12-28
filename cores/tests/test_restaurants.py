import factory
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import UserFactory
from cores.factories import FoodCategoryFactory, RestaurantFactory


class RestaurantAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.owner = UserFactory.create(role='사장')
        self.client.force_authenticate(user=self.owner)

    @classmethod
    def setUpTestData(cls):
        FoodCategoryFactory.create(id=1, type='중식')
        cls.restaurant_info = factory.build(dict, FACTORY_CLASS=RestaurantFactory)

    def test_new_restaurant_should_create(self):
        response = self.client.post('/v1/restaurants', self.restaurant_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_should_not_access_create_restaurant_api(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/v1/restaurants', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_restaurants_should_return_list(self):
        response = self.client.get('/v1/restaurants')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_add_restaurant_should_fail_when_min_order_price_less_than_0(self):
        self.restaurant_info['min_order_price'] = -1000
        response = self.client.post('/v1/restaurants', self.restaurant_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_restaurant_should_fail_when_delivery_price_less_than_0(self):
        self.restaurant_info['delivery_price'] = -1000
        response = self.client.post('/v1/restaurants', self.restaurant_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RestaurantDetailAPITest(APITestCase):
    def setUp(self):
        self.owner = UserFactory.create(role='사장')
        self.other_owner = UserFactory.create(role='사장')
        self.restaurant = RestaurantFactory.create(user=self.owner)
        self.client.force_authenticate(user=self.owner)

    def test_does_not_exist_restaurant_pk_should_return_404(self):
        does_not_exist_restaurant_pk = self.restaurant.id + 1
        response = self.client.get(f'/v1/restaurnats/{does_not_exist_restaurant_pk}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_specific_restaurant_should_return_with_menu_set(self):
        response = self.client.get(f'/v1/restaurants/{self.restaurant.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('menu_set' in response.content.decode())

    def test_update_restaurant_only_can_owner(self):
        update_data = {"name": "change name success"}
        response = self.client.patch(f'/v1/restaurants/{self.restaurant.id}', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], update_data['name'])

    def test_update_restaurant_if_not_owner_should_permission_fail(self):
        self.client.force_authenticate(user=self.other_owner)
        update_data = {"name": "change name success"}
        response = self.client.patch(f'/v1/restaurants/{self.restaurant.id}', update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
