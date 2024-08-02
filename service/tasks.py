
from celery import shared_task
from django.core.mail import send_mail


@shared_task()
def send_reminder_email(subject, message, from_email, to_email, fail_silently=True):
    print("Recipient list:", to_email)
    send_mail(subject, message, from_email, to_email, fail_silently=fail_silently)


@shared_task()
def send_registration_email(subject, message, from_email, to_email, fail_silently=True):
    send_mail(subject, message, from_email, to_email, fail_silently=fail_silently)


@shared_task()
def send_booking_email(subject, message, from_email, to_email, fail_silently=True):
    send_mail(subject, message, from_email, to_email, fail_silently=fail_silently)
