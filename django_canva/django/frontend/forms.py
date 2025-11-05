from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class SignupForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        # Use Django's configured password validators
        validate_password(password)
        return password


