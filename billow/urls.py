"""billow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from accounts.views import accounts, citizen, staff

urlpatterns = [
               path('', include('home.urls', namespace='home')),
               path('bill/', include('bill.urls', namespace='bill')),
               path('accounts/', include('accounts.urls')),
               path('accounts/', include('django.contrib.auth.urls')),
               path('accounts/signup/', accounts.SignUpView.as_view(), name='signup'),
               path('accounts/signup/citizen/', citizen.CitizenSignUpView.as_view(), name='citizen_signup'),
               path('accounts/signup/staff/', staff.StaffSignUpView.as_view(), name='staff_signup'),
               
               path('admin/', admin.site.urls),
               ]
