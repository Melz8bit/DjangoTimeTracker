"""time_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from pages.views import home_view
from timesheet.views import (
    timesheet_list_view
)

from accounts.views import (
    login_view,
    logout_view,
    register_view
)

urlpatterns = [
    path('', timesheet_list_view, name='home'),
    path('login/', login_view, name='login-page'),
    path('logout/', logout_view, name = 'logout'),
    path('register/', register_view, name='register-page'),
    path('admin/', admin.site.urls),
    path('hospitals/', include('hospitals.urls')),
    path('timesheet/', include('timesheet.urls')),
    path('invoice/', include('invoices.urls')),
]
