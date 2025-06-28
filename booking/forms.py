from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CarBooking, Driver
from datetime import datetime

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'phone_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Enter driver name'),
                'type': 'text'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Enter driver phone number'),
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Enter driver email'),
                'type': 'email'
            }),
        }
class BookForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = ['name', 'phone_number', 'email', 'project_number', 'start_date', 'end_date', 'destination', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Enter your name'),
                'type': 'text',
                'required': True
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Enter your phone number'),
                'type': 'tel',
                'required': True
            }),
            'email': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg email-input',
                'placeholder': _('Enter email addresses separated by commas'),
                'rows': 3,
                'required': True
            }),
            'project_number': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Enter project number'),
                'type': 'text',
                'required': True
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'type': 'datetime-local',
                'required': True
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'type': 'datetime-local',
                'required': True
            }),
            'destination': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Select a governorate...'),
                'type': 'text',
                'list': 'governorates',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'required': True
            }),
        }
        def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_date')
            end_date = cleaned_data.get('end_date')
            now = datetime.now()

            if start_date and start_date < now:
                self.add_error('start_date', "Start date cannot be in the past.")

            if start_date and end_date and end_date <= start_date:
                self.add_error('end_date', "End date must be after start date.")

