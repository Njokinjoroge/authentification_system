from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role, BusinessElement, AccessRoleRule
from .serializers import RoleSerializer, BusinessElementSerializer, AccessRoleRuleSerializer

class RoleListCreateView(APIView):
    def get(self, request):
        if not request.user or request.user.role.name != "admin":
            return Response({"error": "Forbidden"}, status=403)
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user or request.user.role.name != "admin":
            return Response({"error": "Forbidden"}, status=403)
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AccessRoleRuleListCreateView(APIView):
    def get(self, request):
        if not request.user or request.user.role.name != "admin":
            return Response({"error": "Forbidden"}, status=403)
        rules = AccessRoleRule.objects.all()
        serializer = AccessRoleRuleSerializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user or request.user.role.name != "admin":
            return Response({"error": "Forbidden"}, status=403)
        serializer = AccessRoleRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

