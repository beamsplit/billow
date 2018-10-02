from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import staff_required
from ..forms import StaffSignUpForm
from ..models import User


class StaffSignUpView(CreateView):
    model = User
    form_class = StaffSignUpForm
    template_name = 'registration/signup_form.html'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('staff:signup')


@method_decorator([login_required, staff_required], name='dispatch')
class ProfileView(ListView):
    model = 'bill.Bill'
    ordering = ('title', )
    context_object_name = 'bill'
    template_name = 'classroom/staff/profile.html'
    
    def get_queryset(self):
        queryset = self.request.user.bill \
            .select_related('category') \
            #.annotate(questions_count=Count('questions', distinct=True)) \
            #.annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset


