from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='home'),
    path('init/', views.GoogleCalendarInitView, name='user auth'),
    path('redirect/', views.GoogleCalendarRedirectView, name='user token'),
]