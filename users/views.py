from rest_framework import generics
from users.models import CustomUser
from users.serializers import UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer