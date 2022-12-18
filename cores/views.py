from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOwnerOrReadOnly, IsMineOrRestaurant, IsMine
from cores.models import Restaurant, Menu, CartItem, Cart, Order
from cores.serializers import RestaurantSerializer, MenuSerializer, CartItemSerializer, CartSerializer, OrderSerializer


class RestaurantAPI(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request):
        queryset = Restaurant.objects.all()
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = RestaurantSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestaurantDetailAPI(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, restaurant_pk):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_pk)
            self.check_object_permissions(self.request, restaurant)
            return restaurant
        except ObjectDoesNotExist:
            return None

    def get(self, request, restaurant_pk):
        restaurant = self.get_object(restaurant_pk)
        if restaurant is None:
            return Response({"message: restaurant pk not exists"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, restaurant_pk):
        user = request.user
        restaurant = self.get_object(restaurant_pk)
        if restaurant is None:
            return Response({"message: restaurant pk not exists"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuAPI(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, restaurant_pk):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_pk)
        except ObjectDoesNotExist:
            return Response({"message: restaurant create first"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetailAPI(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, menu_pk, restaurant):
        try:
            menu = Menu.objects.get(pk=menu_pk)
            if menu.restaurant != restaurant:
                return None
            self.check_object_permissions(self.request, restaurant)
            return menu
        except ObjectDoesNotExist:
            return None

    def get_restaurant(self, restaurant_pk):
        try:
            return Restaurant.objects.get(pk=restaurant_pk)
        except ObjectDoesNotExist:
            return Response({"message: restaurant pk not exists"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, restaurant_pk, menu_pk):
        restaurant = self.get_restaurant(restaurant_pk)
        menu = self.get_object(menu_pk, restaurant)
        if menu is None:
            return Response({"message: menu pk not exists"}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, restaurant_pk, menu_pk):
        restaurant = self.get_restaurant(restaurant_pk)
        menu = self.get_object(menu_pk, restaurant)
        if menu is None:
            return Response({"message: menu pk not exists"}, status=status.HTTP_404_NOT_FOUND)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if Cart.objects.filter(user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "NOT_EXISTS_CART"}, status=status.HTTP_200_OK)

    def post(self, request):
        if Cart.objects.filter(user=request.user).exists():
            cart = Cart.objects.get(user=request.user)
        else:
            cart = Cart.objects.create(user=request.user)

        cart_item = CartItem.objects.filter(cart_id=cart.id, menu=request.data['menu'])
        if cart_item.exists():
            cart_item.update(quantity=request.data['quantity'])
            return Response({"message": "장바구니에 해당 메뉴가 추가되었습니다."}, status=status.HTTP_200_OK)
        else:
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(cart=cart)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if not Cart.objects.filter(user=request.user).exists():
            return Response({'message': 'NOT_EXISTS_CART'}, status=status.HTTP_404_NOT_FOUND)
        cart = Cart.objects.get(user=request.user)
        cart.delete()
        return Response({'message': 'DELETED'}, status=status.HTTP_204_NO_CONTENT)


class CartItemAPI(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        if not CartItem.objects.filter(id=item_id, cart__user=request.user).exists():
            return Response({'message': 'NOT_EXISTS_CART_ITEM'}, status=status.HTTP_404_NOT_FOUND)
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, item_id):
        if not Cart.objects.filter(user=request.user).exists():
            return Response({'message': 'NOT_EXISTS_CART'}, status=status.HTTP_404_NOT_FOUND)
        cart = Cart.objects.get(user=request.user)
        if not CartItem.objects.filter(id=item_id, cart=cart).exists():
            return Response({'message': 'NOT_EXISTS_CART_ITEM'}, status=status.HTTP_404_NOT_FOUND)
        item = CartItem.objects.get(id=item_id, cart=cart)
        item.delete()
        return Response({'message': 'DELETED'}, status=status.HTTP_204_NO_CONTENT)


class OrderAPI(APIView):
    permission_classes = [IsAuthenticated, IsMine]

    def get_object(self, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            self.check_object_permissions(self.request, cart)
            return cart
        except ObjectDoesNotExist:
            return None

    def post(self, request, cart_id):
        cart = self.get_object(cart_id)
        if cart is None or cart.ordered_at is not None:
            return Response({'message': 'INVALID_CART'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPI(APIView):
    permission_classes = [IsAuthenticated, IsMineOrRestaurant]

    def get_object(self, order_id):
        if Order.objects.filter(id=order_id).exists():
            order = Order.objects.get(id=order_id)
            self.check_object_permissions(self.request, order)
            return order
        else:
            return None

    def get(self, request, order_id):
        order = self.get_object(order_id)
        if order is not None:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "NOT_EXISTS_ORDER"}, status=status.HTTP_200_OK)
