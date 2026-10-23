from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
from lms.models import Subscription


@shared_task
def send_course_update_email(course_id):
    """Отправка писем подписчикам при обновлении курса"""
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related('user', 'course')

    for sub in subscriptions:
        send_mail(
            subject=f'Обновление курса: {sub.course.title}',
            message=f'Курс "{sub.course.title}" был обновлён. Проверьте новые материалы!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
            fail_silently=True,
        )

    return f'Отправлено {subscriptions.count()} писем'


@shared_task
def block_inactive_users():
    """Блокировка пользователей, не заходивших более месяца"""
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = CustomUser.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
    )

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f'Заблокировано {count} пользователей'