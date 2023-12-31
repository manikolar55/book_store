# tasks.py

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_purchase_notification(email, purchase_details):
    subject = 'Purchase Notification'
    message = f'Thank you for your purchase!\n\nDetails: {purchase_details}'
    from_email = 'your@email.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
