from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Cart, CartItem
from orders.serializers import CartItemSerializer, CartSerializer


class BlanketAPI(APIView):
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
