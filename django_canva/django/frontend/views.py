from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from .forms import SignupForm
from .templates_catalog import TEMPLATES


def index(request):
    return render(request, 'frontend.html')


def gallery(request):
    return render(request, 'gallery.html')


def templates_view(request):
    return render(request, 'templates_page.html', {"templates": TEMPLATES})


def profile(request):
    if request.user.is_authenticated:
        return redirect('account-profile')
    return render(request, 'profile.html')


@require_POST
def create_profile(request):
    form = SignupForm(request.POST)
    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return render(request, 'profile.html', status=400)

    name = form.cleaned_data['name']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']

    user = User.objects.create_user(username=email, email=email, password=password)
    user.first_name = name
    user.save()
    messages.success(request, 'Account created successfully. You can now log in.')
    return redirect('login')


@login_required
def account_profile(request):
    return render(request, 'account_profile.html')


@require_http_methods(["GET", "POST"]) 
def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

# Create your views here.
