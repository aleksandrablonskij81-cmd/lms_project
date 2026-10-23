import stripe
from django.conf import settings
from users.models import Payment
from lms.models import Course


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course, payment):
    """Создаёт продукт в Stripe и сохраняет ID в платеже"""
    try:
        product = stripe.Product.create(
            name=course.title,
            description=course.description or '',
        )
        payment.stripe_product_id = product.id
        payment.save(update_fields=['stripe_product_id'])
        return product
    except stripe.error.StripeError as e:
        raise Exception(f'Ошибка создания продукта: {str(e)}')


def create_stripe_price(product_id, amount):
    """Создаёт цену в Stripe (в копейках)"""
    try:
        price = stripe.Price.create(
            unit_amount=int(amount * 100),
            currency='rub',
            product=product_id,
        )
        return price
    except stripe.error.StripeError as e:
        raise Exception(f'Ошибка создания цены: {str(e)}')


def create_checkout_session(course, payment, success_url, cancel_url):
    """Создаёт сессию оплаты и возвращает ссылку"""
    try:
        product = create_stripe_product(course, payment)
        price = create_stripe_price(product.id, course.price)
        payment.stripe_price_id = price.id
        payment.save(update_fields=['stripe_price_id'])

        session = stripe.checkout.Session.create(

            line_items=[{
                'price': price.id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            managed_payments={'enabled': False},  # 👈 ДОБАВИТЬ ЭТУ СТРОКУ

        )

        payment.stripe_session_id = session.id
        payment.payment_url = session.url
        payment.save(update_fields=['stripe_session_id', 'payment_url'])

        return session
    except stripe.error.StripeError as e:
        raise Exception(f'Ошибка создания сессии: {str(e)}')