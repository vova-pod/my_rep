"""Defines URL patterns for web_travel_data"""

from django.urls import path

from . import views

app_name = 'web_travel_data'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

]
