from django.contrib.auth import authenticate, logout
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserSerializer


class RegisterAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"Token": token.key}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"Message": "Logout success"}, status=status.HTTP_202_ACCEPTED)


