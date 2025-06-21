from django.db import models

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
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    destination = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=status, default='pending', null=True, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
    
    def get_emails_list(self):
        """Return a list of email addresses from the email field"""
        if not self.email:
            return []
        # Split by comma and clean up whitespace
        emails = [email.strip() for email in self.email.split(',') if email.strip()]
        return emails