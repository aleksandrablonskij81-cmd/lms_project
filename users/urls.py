from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserUpdateAPIView, PaymentViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('', include(router.urls)),
]