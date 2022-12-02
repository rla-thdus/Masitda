from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsMine
from orders.models import Cart, BlanketItem
from orders.serializers import BlanketItemSerializer, BlanketSerializer
from users.models import User


class BlanketAPI(APIView):
    permission_classes = [IsAuthenticated, IsMine]

    def get(self, request, user_id):
        if Cart.objects.filter(user_id=user_id).exists():
            blanket = Cart.objects.get(user_id=user_id)
            serializer = BlanketSerializer(blanket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "BLANKET_NOT_EXISTS"}, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        if Cart.objects.filter(user_id=user_id).exists():
            blanket = Cart.objects.get(user_id=user_id)
        else:
            blanket = Cart.objects.create(user=request.user)

        blanket_item = BlanketItem.objects.filter(blanket_id=blanket.id, menu=request.data['menu'])
        if blanket_item.exists():
            blanket_item.update(quantity=request.data['quantity'])
            return Response({"message": "장바구니에 해당 메뉴가 추가되었습니다."}, status=status.HTTP_200_OK)
        else:
            serializer = BlanketItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(blanket=blanket)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

