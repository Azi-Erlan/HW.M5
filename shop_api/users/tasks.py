from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@shared_task
def send_test_email():

    send_mail(
        subject="Celery Test",
        message="Мой тестовый email через Celery",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["your_email@gmail.com"],
        fail_silently=False,
    )

    return "OK"

@shared_task
def print_hello():
    print(f'Celery работает! Время: {timezone.now()}')


@shared_task
def add(x, y):
    print(f"<----------args {x} and {y}---------->")
    # from time import sleep

    # sleep(15)
    return x + y


@shared_task
def send_otp_email(email, otp):
    print("sending" * 10)
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is: {otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    return "OK"


@shared_task
def send_report_email():
    print("sending" * 10)
    send_mail(
        subject="Report data",
        message="Важное",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            "bkaizirek2002@gmail.com",
            "abdillaevamedina6@gmail.com",
        ],
        fail_silently=False,
    )
    return "OK"