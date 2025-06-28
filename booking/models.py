from django.db import models
import random

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=16)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class CarBooking(models.Model):
    status = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=16)
    email = models.TextField(max_length=500)
    project_number = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    destination = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=status, default='pending', null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    
    # New fields for trip confirmation system
    confirmation_code = models.CharField(max_length=4, null=True, blank=True)
    client_confirmed = models.BooleanField(default=False)
    admin_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.status}"
    
    def get_emails_list(self):
        """Return a list of email addresses from the email field"""
        if not self.email:
            return []
        # Split by comma and clean up whitespace
        emails = [email.strip() for email in self.email.split(',') if email.strip()]
        return emails
    
    def generate_confirmation_code(self):
        """Generate a random 4-digit confirmation code"""
        self.confirmation_code = str(random.randint(1000, 9999))
        self.save()
        return self.confirmation_code
    
    def check_completion_status(self):
        """Check if both client and admin have confirmed, and update status if needed"""
        if self.client_confirmed and self.admin_confirmed and self.status != 'completed':
            self.status = 'completed'
            self.save()
            return True
        return False