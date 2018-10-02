from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from django.urls import resolve
from home.views import IndexView


# Create your tests here.


class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_index_view(self):
        request = RequestFactory().get('/home')
        view = IndexView.as_view(template_name='index.html')

        # Run.
        response = view(request)
        # Check.
        self.assertEqual(response.status_code, 200)




    
