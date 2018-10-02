from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView


# Create your views here

from accounts.decorators import citizen_required
from bill.models import Bill, Category
from accounts.forms import CitizenInterestsForm, CitizenSignUpForm
from accounts.models import Citizen, CitizenBill, User


class IndexView(ListView):
    model = Bill
    ordering = ('title', )
    context_object_name = 'selected_bill'
    template_name = 'index.html'
    
    def get_queryset(self):
        queryset = Bill.objects.all()
        queryset = queryset[:10]
        return queryset

class AboutView(ListView):
    model = Bill
    template_name = 'about.html'

class ContactView(ListView):
    model = Bill
    template_name = 'contact.html'

