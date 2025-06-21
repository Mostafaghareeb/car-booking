from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CarBooking
from .email_module import *

@receiver(pre_save, sender=CarBooking)
def trip_status_change(sender, instance, **kwargs):

    if not instance.pk:
        return

    old_trip = CarBooking.objects.get(pk=instance.pk)

    if old_trip.status != instance.status:
        # Get all email addresses for this trip
        email_list = instance.get_emails_list()
        
        if instance.status == 'active':
            # Generate confirmation code if not already present
            if not instance.confirmation_code:
                instance.confirmation_code = str(instance.generate_confirmation_code())
            
            for email in email_list:
                send_trip_approved_email(
                    user_name=instance.name,
                    user_email=email,
                    destination=instance.destination,
                    confirmation_code=instance.confirmation_code,
                )
        elif instance.status == 'cancelled':
            for email in email_list:
                send_trip_cancelled_email(
                    user_name=instance.name,
                    user_email=email,
                    destination=instance.destination,
                )