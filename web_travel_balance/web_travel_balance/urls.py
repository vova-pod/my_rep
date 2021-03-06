"""web_travel_balance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from . import version
from web_travel_data import views as wtd_views


urlpatterns = [path('sw.js', wtd_views.ServiceWorkerView.as_view(),
                    name=wtd_views.ServiceWorkerView.name,
                    ),
               ]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('web_travel_data.urls')),
    path('', include('django.contrib.auth.urls')),
    path('rosetta/', include('rosetta.urls')),
)
