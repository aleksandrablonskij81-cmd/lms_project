from rest_framework import viewsets, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.models import CustomUser, Payment
from users.serializers import UserSerializer, PaymentSerializer, RegisterSerializer
from users.filters import PaymentFilter


class UserViewSet(viewsets.ModelViewSet):
    """CRUD пользователей. Обычный пользователь видит только себя."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['email', 'id']
    ordering = ['id']

    def get_permissions(self):
        # Регистрация доступна всем
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def get_queryset(self):
        # Админ/персонал видит всех, остальные — только себя
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class PaymentViewSet(viewsets.ModelViewSet):
    """Платежи с фильтрацией и сортировкой. Обычный пользователь видит только свои."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']

    def get_queryset(self):
        # Админ/персонал видит все платежи, остальные — только свои
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновление профиля (оставлено для совместимости)."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]