from django.urls import include, path

from .views import accounts, citizen, staff

urlpatterns = [path('', accounts.home, name='home'),
               path('citizen/', include(([
                                        path('', citizen.ProfileView.as_view(), name='profile'),
                                           path('interests/', citizen.CitizenInterestsView.as_view(), name='citizen_interests'),
                                           ], 'accounts'), namespace='citizen')),

               ]
