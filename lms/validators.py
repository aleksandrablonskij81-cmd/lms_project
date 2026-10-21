from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_youtube_url(value):
    """Валидатор: ссылка должна вести только на youtube.com"""
    if not value:
        return  # пустое значение разрешено (blank=True)

    parsed = urlparse(value)
    domain = parsed.netloc.lower()

    # Разрешаем youtube.com и www.youtube.com
    if domain not in ('youtube.com', 'www.youtube.com', 'youtu.be', 'www.youtu.be'):
        raise ValidationError(
            'Ссылка должна вести только на YouTube (youtube.com). '
            'Ссылки на сторонние ресурсы запрещены.'
        )