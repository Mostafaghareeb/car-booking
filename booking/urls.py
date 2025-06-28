from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('book', views.book, name='book'),
    path('search/', views.search, name='search'),
    path('client-confirm/<int:trip_id>/', views.client_confirm_trip, name='client_confirm_trip'),
    path('delete-trip/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('trips/', views.trips, name='trips'),  
    path('trips/update/<int:trip_id>/', views.update_trip_status, name='update_trip_status'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
]               