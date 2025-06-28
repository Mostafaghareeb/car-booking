from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib import messages
from .forms import *
from .models import CarBooking
from django.utils import timezone
from background_task import background
from .email_module import send_pending_email, send_driver_assigned_email_to_client, send_trip_details_email_to_driver, send_trip_approved_email


@background(schedule=1)
def send_pending_email_task(user_name, user_email, user_destination, user_start_date, user_end_date, confirmation_code):
    send_pending_email(user_name, user_email, user_destination, user_start_date, user_end_date, confirmation_code)


def index(request): 
    return render(request, 'pages/index.html')


def book(request):
    if request.method == 'POST':
        book_info = BookForm(request.POST)
        if book_info.is_valid():
            trip = book_info.save()
            
            # Generate confirmation code
            confirmation_code = trip.generate_confirmation_code()

            user_name = request.POST.get("name")
            user_emails = request.POST.get("email")
            user_start_date = request.POST.get("start_date")
            user_end_date = request.POST.get("end_date")
            user_destination = request.POST.get("destination")
            
            # Send email to all provided email addresses
            if user_emails:
                email_list = [email.strip() for email in user_emails.split(',') if email.strip()]
                for email in email_list:
                    send_pending_email_task(user_name, email, user_destination, user_start_date, user_end_date, confirmation_code)

            return redirect('index')
        else:
            print(book_info.errors)
    return render(request, 'pages/book.html', {'form': BookForm()})



def search(request):

    context = {
        'trips': CarBooking.objects.all(),
        'has_data': CarBooking.objects.exists(),
        'latest_trips': CarBooking.objects.order_by('start_date')[:10]
    }
    return render(request, 'pages/search.html', context)


def client_confirm_trip(request, trip_id):
    """Handle client trip confirmation with code"""
    if request.method == 'POST':
        trip = get_object_or_404(CarBooking, id=trip_id)
        entered_code = request.POST.get('confirmation_code')
        
        if trip.confirmation_code and entered_code == trip.confirmation_code:
            trip.client_confirmed = True
            trip.save()
            
            # Check if both client and admin have confirmed
            trip.check_completion_status()
            
            messages.success(request, 'Trip confirmed successfully!')
        else:
            messages.error(request, 'Invalid confirmation code. Please try again.')
    
    return redirect('search')


def dashboard(request):
    # Get trip statistics
    total_trips = CarBooking.objects.count()
    pending_trips = CarBooking.objects.filter(status='pending').count()
    active_trips = CarBooking.objects.filter(status='active').count()
    cancelled_trips = CarBooking.objects.filter(status='cancelled').count()
    completed_trips = CarBooking.objects.filter(status='completed').count()
    
    # Get recent trips
    recent_trips = CarBooking.objects.order_by('-created_at')[:5]

    today = timezone.now().date()
    dates = [today - timezone.timedelta(days=i) for i in range(4, -1, -1)]
    date_labels = [d.strftime('%b %d') for d in dates]

    trip_counts = []
    for date in dates:
        count = CarBooking.objects.filter(start_date=date).count()
        trip_counts.append(count)
    
    context = {
        'total_trips': total_trips,
        'pending_trips': pending_trips,
        'active_trips': active_trips,
        'cancelled_trips': cancelled_trips,
        'completed_trips': completed_trips,
        'recent_trips': recent_trips,
        'labels': date_labels,
        'data': trip_counts
    }
    
    return render(request, 'dashboard/dashboard.html', context)


def trips(request):
    # Get all trips
    trips = CarBooking.objects.all().order_by('-created_at')
    
    context = {
        'trips': trips,
    }
    
    return render(request, 'dashboard/trips.html', context)


def update_trip_status(request, trip_id):
    if request.method == "POST":
        trip = get_object_or_404(CarBooking, id=trip_id)
        action = request.POST.get('action')

        if trip.status in ['completed', 'cancelled']:
            messages.warning(request, f"The trip status cannot be modified because it is {trip.status}.")
            return redirect('trips')

        if action == 'approved' and trip.status == 'pending':
            trip.status = 'active'
        elif action == 'cancelled':
            trip.status = 'cancelled'
        elif action == 'completed':
            trip.admin_confirmed = True
            trip.save()
            trip.check_completion_status()

        trip.save()
        messages.success(request, "Trip status updated successfully.")
    return redirect('trips')


def trip_detail(request, trip_id):
    trip = get_object_or_404(CarBooking, id=trip_id)
    
    if request.method == 'POST':
        trip_form = BookForm(request.POST, instance=trip, prefix='trip')
        driver_form = DriverForm(request.POST, prefix='driver')
        
        if trip_form.is_valid() and driver_form.is_valid():
            # Save trip changes
            updated_trip = trip_form.save()
            
            # Save or update driver
            driver = driver_form.save()
            updated_trip.driver = driver
            updated_trip.save()
            
            # Send emails
            trip_details = {
                'destination': updated_trip.destination,
                'start_date': updated_trip.start_date,
                'end_date': updated_trip.end_date,
            }
            
            # Send email to client
            client_emails = updated_trip.get_emails_list()
            for client_email in client_emails:
                send_driver_assigned_email_to_client(
                    updated_trip.name,
                    client_email,
                    driver.name,
                    driver.phone_number,
                    driver.email,
                    trip_details
                )
            
            # Send email to driver
            send_trip_details_email_to_driver(
                driver.name,
                driver.email,
                updated_trip.name,
                updated_trip.phone_number,
                client_emails[0] if client_emails else '',
                trip_details
            )
            
            messages.success(request, 'Trip and driver information saved successfully.')
            return redirect('trips')

    else:
        trip_form = BookForm(instance=trip, prefix='trip')
        if trip.driver:
            driver_form = DriverForm(instance=trip.driver, prefix='driver')
        else:
            driver_form = DriverForm(prefix='driver')
    
    context = {
        'trip': trip,
        'trip_form': trip_form,
        'driver_form': driver_form,
    }
    
    return render(request, 'dashboard/trip_detail.html', context)


def delete_trip(request, trip_id):
    """Handle trip deletion with confirmation code verification"""
    if request.method == 'POST':
        trip = get_object_or_404(CarBooking, id=trip_id)
        entered_code = request.POST.get('confirmation_code')
        
        if trip.confirmation_code and entered_code == trip.confirmation_code:
            trip.status = 'cancelled'
            trip.save()
            messages.success(request, 'Trip cancelled successfully!')
        else:
            messages.error(request, 'Invalid confirmation code. Please try again.')
    
    return redirect('search')
