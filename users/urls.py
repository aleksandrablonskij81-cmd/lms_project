from django.urls import path
from users.views import UserUpdateAPIView

app_name = 'users'

urlpatterns = [
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
]