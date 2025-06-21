from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('book', views.book, name='book'),
    path('cancel', views.cancel, name='cancel'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('search', views.search, name='search'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('trips/', views.trips, name='trips'),  
    path('trips/update/<int:trip_id>/', views.update_trip_status, name='update_trip_status'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
]