from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.html import escape, mark_safe

from django.db.models.signals import post_save
from django.dispatch import receiver

from scripts.locations import *

from bill.models import Bill, Category

class User(AbstractUser):
    is_citizen = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)



class CitizenCategory(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=30, choices=LOCATION_CHOICES, default='1')
    email = models.EmailField(max_length=300,default='')
    my_bills = models.ManyToManyField(Bill, through='CitizenBill')
    interests = models.ManyToManyField(Category, related_name='interested_citizens')
    favourites = models.ManyToManyField(Bill, related_name='favourited_by')
    
    def __str__(self):
        return self.user.username


class CitizenBill(models.Model):
    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='selected_bill', null=True, blank=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='selected_bill', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

class FavouritesModel(models.Model):
    user = models.ForeignKey(Citizen, on_delete=models.SET_NULL, null=True)
    favourited_bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

