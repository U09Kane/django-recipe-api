from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """creates a new user in the system"""
    serializer_class = UserSerializer
