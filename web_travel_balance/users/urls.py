""" Defines URL patterns for users app"""

from django.urls import path, include
from .views import SignUpView, ActivateAccount

from . import views

app_name = 'users'

urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/',
         ActivateAccount.as_view(), name='activate'),
]
