from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


from . import views
from .views import BillDetailView, DeputyDetailView, TagsView, BillSearchView, TDListView, FavouritesFormView

app_name = 'bill'
urlpatterns = [
               path('', views.index, name='index'),
               path('tags/', TagsView.as_view(), name='tags'),
               path('search/', BillSearchView.as_view(), name='bill-search'),
               path('deputy/<int:pk>', DeputyDetailView.as_view(), name='deputy-detail'),
               path('deputy/', TDListView.as_view(), name='td-list'),
               path('bills/<int:pk>/', BillDetailView.as_view(), name='detail'),
               url(r'^bills/(?P<pk>\d+)/movement/$', views.add_movement, name='add_movement'),
               path('bills/<int:pk>/create_post/', views.create_post, name='create-post'),
               
               ]



