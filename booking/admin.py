from django.contrib import admin
from .models import CarBooking, Driver

@admin.register(CarBooking)
class CarBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'start_date', 'end_date', 'status', 'client_confirmed', 'admin_confirmed', 'created_at')
    list_filter = ('status', 'client_confirmed', 'admin_confirmed', 'start_date', 'created_at')
    search_fields = ('name', 'destination', 'email', 'phone_number')
    readonly_fields = ('confirmation_code', 'created_at')
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('name', 'phone_number', 'email', 'destination', 'start_date', 'end_date', 'status')
        }),
        ('Driver Assignment', {
            'fields': ('driver',),
            'classes': ('collapse',)
        }),
        ('Confirmation System', {
            'fields': ('confirmation_code', 'client_confirmed', 'admin_confirmed'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'created_at')
    search_fields = ('name', 'phone_number', 'email')
    readonly_fields = ('created_at', 'updated_at')