from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsOwnerOnly
from restaurants.models import Restaurant, Menu
from restaurants.serializers import RestaurantSerializer, MenuSerializer


class RestaurantAPI(APIView):
    permission_classes = [IsOwnerOnly]

    def get(self, request):
        queryset = Restaurant.objects.filter(user=request.user.id)
        serializer = RestaurantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = RestaurantSerializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuAPI(APIView):
    permission_classes = [IsOwnerOnly]

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
    permission_classes = [IsOwnerOnly]
    serializer_class = MenuSerializer

    def put(self, request, restaurant_pk, menu_pk):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_pk)
        except ObjectDoesNotExist:
            return Response({"message: restaurant create first"}, status=status.HTTP_404_NOT_FOUND)
        menu = Menu.objects.get(pk=menu_pk)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
