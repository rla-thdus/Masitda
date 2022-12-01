from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Blanket, BlanketItem
from orders.serializers import BlanketItemSerializer, BlanketSerializer


class BlanketAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if Blanket.objects.filter(user_id=user_id).exists():
            blanket = Blanket.objects.get(user_id=user_id)
            serializer = BlanketSerializer(blanket)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "BLANKET_NOT_EXISTS"}, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        if Blanket.objects.filter(user_id=user_id).exists():
            blanket = Blanket.objects.get(user_id=user_id)
        else:
            blanket = Blanket.objects.create(user=request.user)

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

