from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from auth.serializers import RegisterSerializer, LoginSerializer
from auth.helpers import get_token_for_user

class RegisterAPI(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Please Enter Valid Email and Password.', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                response_data = get_token_for_user(user)
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid Email or Password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'message': 'Bad Request', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
