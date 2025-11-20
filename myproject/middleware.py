import jwt
from django.conf import settings
from users.models import User

# Replace with your actual secret key from settings
SECRET_KEY = "YOUR_SECRET_KEY"

class AuthMiddleware:
    """
    Middleware to authenticate user via JWT token in Authorization header:
    Authorization: Bearer <token>
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get("Authorization")
        request.user = None

        if token and token.startswith("Bearer "):
            token = token.split("Bearer ")[1]
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                # Fetch the user from DB
                request.user = User.objects.get(id=data["user_id"], is_active=True)
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                request.user = None

        response = self.get_response(request)
        return response
