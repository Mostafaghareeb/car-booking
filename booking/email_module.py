from django.core.mail import send_mail
from django.conf import settings

def send_pending_email(user_name, user_email, user_destination, user_start_date, user_end_date):
    subject = "Trip Booking Request Received"

    message = f"""
Hello {user_name},

Your request to book a trip has been received.

Destination: {user_destination}  
Start Date: {user_start_date}  
End Date: {user_end_date}  

Current Status: Pending Review

Our team will review your request and contact you once it is approved or if any further information is required.

Regards,  
Customer Support Team
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )


def send_trip_approved_email(user_name, user_email, destination, confirmation_code):
    subject = "Your Trip Has Been Approved ✅"
    message = f"""
Dear {user_name},

We are pleased to inform you that your trip to {destination} has been approved and is now active.

You can now start preparing for your journey. If you have any questions or need assistance, feel free to reach out to our support team.

IMPORTANT: Your Trip Confirmation Code
Your unique 4-digit confirmation code is: **{confirmation_code}**

You will need this code later to confirm and complete your trip. Please keep this code safe and do not share it with anyone.

Best regards,  
Customer Support Team
"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message.strip(), from_email, recipient_list)



def send_trip_cancelled_email(user_name, user_email, destination):
    subject = "Your Trip Has Been Cancelled ❌"
    message = f"""
Dear {user_name},

We regret to inform you that your trip to {destination} has been cancelled.

If you believe this was a mistake or have any questions, please contact our support team for further assistance.

Sincerely,  
Customer Support Team
"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message.strip(), from_email, recipient_list)


def send_driver_assigned_email_to_client(client_name, client_email, driver_name, driver_phone, driver_email, trip_details):
    subject = "Driver Assigned to Your Trip 🚗"
    message = f"""
Dear {client_name},

A driver has been assigned to your trip. Here are the details:

Driver Information:
- Name: {driver_name}
- Phone: {driver_phone}
- Email: {driver_email}

Trip Details:
- Destination: {trip_details['destination']}
- Start Date: {trip_details['start_date']}
- End Date: {trip_details['end_date']}

Please contact your driver directly to coordinate pickup details and any specific requirements.

Best regards,
Customer Support Team
"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [client_email]

    send_mail(subject, message.strip(), from_email, recipient_list)


def send_trip_details_email_to_driver(driver_name, driver_email, client_name, client_phone, client_email, trip_details):
    subject = "New Trip Assignment 🚗"
    message = f"""
Dear {driver_name},

You have been assigned a new trip. Here are the details:

Client Information:
- Name: {client_name}
- Phone: {client_phone}
- Email: {client_email}

Trip Details:
- Destination: {trip_details['destination']}
- Start Date: {trip_details['start_date']}
- End Date: {trip_details['end_date']}

Please contact the client to coordinate pickup details and any specific requirements.

Best regards,
Customer Support Team
"""
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [driver_email]

    send_mail(subject, message.strip(), from_email, recipient_list)
