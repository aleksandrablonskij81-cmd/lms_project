from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Менеджер для кастомного пользователя"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя с email как логином"""
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватарка')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Платёж за курс или урок"""
    PAYMENT_CASH = 'cash'
    PAYMENT_TRANSFER = 'transfer'

    PAYMENT_CHOICES = [
        (PAYMENT_CASH, 'Наличные'),
        (PAYMENT_TRANSFER, 'Перевод на счёт'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидает'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_FAILED, 'Ошибка'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )
    course = models.ForeignKey(
        'lms.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный курс'
    )
    lesson = models.ForeignKey(
        'lms.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный урок'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default=PAYMENT_TRANSFER,
        verbose_name='Способ оплаты'
    )

    # Поля для Stripe
    stripe_product_id = models.CharField(max_length=255, blank=True)
    stripe_price_id = models.CharField(max_length=255, blank=True)
    stripe_session_id = models.CharField(max_length=500, blank=True)  # 👈 увеличили
    payment_url = models.URLField(max_length=500, blank=True)  # 👈 увеличили

    # 👇 СТАТУС (его не хватало)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='Статус оплаты'
    )

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']

    def __str__(self):
        return f'{self.user.email} — {self.amount} ({self.payment_method})'