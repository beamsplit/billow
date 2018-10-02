from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff:quiz_change_list')
        else:
            return redirect('citizen:profile')
    return render(request, 'home/index.html')
