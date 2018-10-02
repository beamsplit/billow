import json
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView, FormView
from django.views import View
from django.urls import reverse_lazy

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, get_list_or_404
from django.template import loader


# Create your views here

from .models import Bill, Category, AssociatedAct, Sponsor, Deputy, Senator, Constituency, Party, Panel, Movement
from .forms import MovementForm
from accounts.models import User, Citizen, FavouritesModel
from accounts.forms import FavouritesForm

def index(request):
    bill_list = Bill.objects.all().order_by('-date')
    bill_count = Bill.objects.all().count()
    category_list = Category.objects.all()
    template = loader.get_template('home/index.html')
    context = {'bill_list': bill_list,'bill_count': bill_count, 'category_list': category_list}
    return HttpResponse(template.render(context, request))


class TagsView(ListView):
    model = Bill
    template_name = 'bill/tags/tags.html'

    def get_context_data(self, **kwargs):
        context = super(TagsView, self).get_context_data(**kwargs)
        context['bill_list'] = Bill.objects.all().exclude(bill_history = 'Enacted').exclude(bill_history = 'Defeated').exclude(bill_history = 'Lapsed').exclude(bill_history = 'Withdrawn').order_by('-date')
        context['category_list'] = Category.objects.all()
        return context
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Bill.objects.filter(title__icontains=query).order_by('-date')
        else:
            return Bill.objects.all().order_by('-date')

class TDListView(ListView):
    model = Deputy
    template_name = 'bill/politicians/tds.html'
    
    def get_context_data(self, **kwargs):
        context = super(TDListView, self).get_context_data(**kwargs)
        context['td_list'] = Deputy.objects.all().order_by('constituency__name')
        return context

class BillSearchView(ListView):
    template_name = 'bill/tags/bill_search.html'
    model = Bill
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Bill.objects.filter(title__icontains=query).order_by('-date')
        else:
            return Bill.objects.all().order_by('-date')

class BillDetailView(DetailView):
    model = Bill
    template_name = 'bill/bills/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(BillDetailView, self).get_context_data(**kwargs)
        context['td'] = Deputy.objects.all()
        context['constituency'] = Constituency.objects.all()
        context['citizens'] = Citizen.objects.all()
        context['associated_act'] = AssociatedAct.objects.all()
        context['bill_list'] = Bill.objects.all()
        context['form'] = FavouritesForm
        return context

def create_post(request, pk):
    if request.is_ajax():
        citizen = Citizen.objects.get(user=request.user)

        bill = Bill.objects.get(pk=pk)
        
        # delete it if it's already a favourite
        if citizen.favourites.filter(id = bill.id):
            citizen.favourites.remove(bill)
            status = 'removed'

        # otherwise, create it
        else:
            citizen.favourites.add(bill)
            status = 'added'

        response = {'status': status,
                    'fav_count': citizen.favourites.filter(title = bill.title).count()}

        return HttpResponse(json.dumps(response, ensure_ascii=False),
                            content_type='application/json')

    return HttpResponse(status=405)

class FavouritesFormView(FormView):
    template_name = 'bill/bills/detail.html'
    form_class = FavouritesForm
    success_url = 'bill/bills/detail.html'
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super().form_valid(form)


class DeputyDetailView(DetailView):
    model = Deputy
    template_name = 'bill/politicians/deputy_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DeputyDetailView, self).get_context_data(**kwargs)
        context['bill'] = Bill.objects.all().order_by('-date')
        context['sponsor'] = Sponsor.objects.all()
        context['constituency'] = Constituency.objects.all()
        return context

def add_movement(request, pk):
    bill = Bill.objects.get(pk=pk)
    
    if request.method == "POST":
        form = MovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.bill = bill
            movement.save()
            movement.author = request.user
            movement.save()
            return redirect('bill:detail', pk=bill.pk)
    else:
        form = MovementForm()
    return render(request, 'bill/bills/add_movement.html', {'form': form})




