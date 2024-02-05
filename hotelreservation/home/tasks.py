# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Booking
import logging
logger = logging.getLogger(__name__)
@shared_task
def send_booking_confirmation_email(booking_id,email):
    try:
        booking = Booking.objects.get(pk=booking_id)
        logger.info(f'Starting send_booking_confirmation_email task for booking ID {booking_id}')
        subject = 'Booking Confirmation'
        message = f'Thank you for your booking. Your booking ID is {booking_id}.'
        from_email = 'luxestayuae@gmail.com'  # Update with your email
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        logger.info(f'Email sent successfully for booking ID {booking_id}')
    except Booking.DoesNotExist:
        logger.error(f'Booking does not exist for ID {booking_id}')
        # Handle the case where the booking does not exist
    except Exception as e:
        logger.error(f'Error sending email for booking ID {booking_id}: {str(e)}')
