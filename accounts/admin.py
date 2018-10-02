from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Citizen, CitizenBill, User
from bill.models import Bill, Category

admin.site.register(User)
admin.site.register(Citizen)
