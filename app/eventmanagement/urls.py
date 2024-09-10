from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.createEvent, name='create'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('api/get_events/', views.get_user_events, name='get-events'),
    path('event/<int:event_id>/', views.event_page, name='event-page'),
]