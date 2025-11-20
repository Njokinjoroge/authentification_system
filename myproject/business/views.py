from rest_framework.views import APIView
from rest_framework.response import Response
from permissions_app.utils import check_permission

class ProductsView(APIView):
    def get(self, request):
        if not request.user:
            return Response({"error": "Unauthorized"}, status=401)

        if not check_permission(request.user, "products", "read"):
            return Response({"error": "Forbidden"}, status=403)

        return Response([
            {"id": 1, "name": "Laptop"},
            {"id": 2, "name": "Phone"}
        ])
