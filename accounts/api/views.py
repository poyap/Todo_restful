from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework import permissions
from .serializers import UserSerializer


class SignUpAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]