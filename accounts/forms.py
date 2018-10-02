from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from accounts.models import Citizen, CitizenBill, CitizenCategory, User
from bill.models import Bill, Category

from scripts.locations import *


class StaffSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class CitizenSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
                                               queryset=Category.objects.all(),
                                               widget=forms.CheckboxSelectMultiple,
                                               required=False
                                               )
    location = forms.ChoiceField(
                                 choices=LOCATION_CHOICES,
                                 widget=forms.Select,
                                 required=False
                                 )
    email = forms.EmailField(max_length=300,required=True)
    
        
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email','location',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_citizen = True
        user.save()
        citizen = Citizen.objects.create(user=user)
        citizen.email = self.cleaned_data.get('email')
        citizen.interests.add(*self.cleaned_data.get('interests'))
        citizen.location = self.cleaned_data.get('location')
        citizen.save()
        return user


class CitizenInterestsForm(forms.ModelForm):
    class Meta:
        model = Citizen
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

class FavouritesForm(forms.ModelForm):
    class Meta:
        model = Citizen
        fields = ('favourites', )
        widgets = {
            'favourites': forms.CheckboxSelectMultiple
        }

