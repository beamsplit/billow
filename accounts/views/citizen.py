from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from ..decorators import citizen_required
from ..forms import CitizenInterestsForm, CitizenSignUpForm
from ..models import Citizen, CitizenBill, User
from bill.models import Bill, Category


class CitizenSignUpView(CreateView):
    model = User
    form_class = CitizenSignUpForm
    template_name = 'registration/signup_form.html'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Citizen'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('citizen:profile')


@method_decorator([login_required, citizen_required], name='dispatch')
class CitizenInterestsView(UpdateView):
    model = Citizen
    form_class = CitizenInterestsForm
    template_name = 'accounts/citizen/interests_form.html'
    success_url = reverse_lazy('citizen:profile')
    
    def get_object(self):
        return self.request.user.citizen
    
    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, citizen_required], name='dispatch')
class ProfileView(ListView):
    model = Bill
    ordering = ('title', )
    template_name = 'accounts/citizen/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        citizen = self.request.user.citizen
        citizen_interests = citizen.interests.values_list('pk', flat=True)
        citizen_favourites = citizen.favourites.values_list('pk', flat=True)
        context['interested_bills'] = Bill.objects.filter(category__in=citizen_interests).exclude(bill_history = 'Enacted').exclude(bill_history = 'Defeated').exclude(bill_history = 'Lapsed').exclude(bill_history = 'Withdrawn').order_by('-date')
        context['fave_bills'] = Bill.objects.filter(id__in=citizen_favourites).order_by('-date')
        context['all_bills'] = Bill.objects.all().order_by('-date')
        return context


