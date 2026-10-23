from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, SubscriptionAPIView, CreatePaymentView

app_name = 'lms'


@csrf_exempt
def payment_success(request):
    """Страница успешной оплаты (редирект от Stripe)"""
    return JsonResponse({
        'status': 'success',
        'message': 'Оплата прошла успешно!'
    })


@csrf_exempt
def payment_cancel(request):
    """Страница отмены оплаты (редирект от Stripe)"""
    return JsonResponse({
        'status': 'cancel',
        'message': 'Оплата отменена.'
    })


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription'),
    path('payments/create/', CreatePaymentView.as_view(), name='payment-create'),
    path('payments/success/', payment_success, name='payment-success'),
    path('payments/cancel/', payment_cancel, name='payment-cancel'),
]