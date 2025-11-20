from django.shortcuts import render
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer
import jwt
from django.conf import settings



SECRET_KEY = "YOUR_SECRET_KEY"

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created"}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        if user.check_password(password):
            token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
            return Response({"token": token})
        return Response({"error": "Invalid credentials"}, status=401)

class LogoutView(APIView):
    def post(self, request):
        # JWT stateless logout → client deletes token
        return Response({"message": "Logged out"}, status=200)

class UserUpdateView(APIView):
    def patch(self, request):
        user = request.user
        if not user:
            return Response(status=401)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class UserDeleteView(APIView):
    def delete(self, request):
        user = request.user
        if not user:
            return Response(status=401)
        user.is_active = False
        user.save()
        return Response({"message": "User soft deleted"}, status=200)
