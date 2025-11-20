from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class BusinessObjectList(APIView):
    """
    Return a list of fictional business objects.
    """
    def get(self, request):
        # Fake data
        data = [
            {"id": 1, "name": "Object A"},
            {"id": 2, "name": "Object B"},
            {"id": 3, "name": "Object C"},
        ]
        # TODO: check permissions in real access control
        return Response(data)
