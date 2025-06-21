from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CarBooking, Driver

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
        fields = ['name', 'phone_number', 'email', 'start_date', 'end_date', 'destination', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Enter your name'),
                'type': 'text'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Enter your phone number'),
                'type': 'tel'
            }),
            'email': forms.Textarea(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg email-input',
                'placeholder': _('Enter email addresses separated by commas'),
                'rows': 3
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'type': 'date',
            }),
            'destination': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
                'placeholder': _('Select a governorate...'),
                'type': 'text',
                'list': 'governorates'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-lg',
            }),
        }

