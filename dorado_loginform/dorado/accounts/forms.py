import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email", "autofocus": True}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password", "autocomplete": "current-password"}),
    )
    remember_me = forms.BooleanField(required=False, label="Remember me")

    error_messages = {
        "invalid_login": "Incorrect email or password. Check your details and try again.",
        "inactive": "This account is inactive.",
    }


class RegisterForm(forms.Form):
    full_name = forms.CharField(
        label="Full name", max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Enter your full name", "autocomplete": "name"}),
    )
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
    )
    password = forms.CharField(
        label="Password", strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Create a password", "autocomplete": "new-password"}),
    )
    confirm_password = forms.CharField(
        label="Confirm password", strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Re-enter your password", "autocomplete": "new-password"}),
    )
    terms = forms.BooleanField(
        required=True,
        error_messages={"required": "You need to agree to the Terms of service and Privacy policy."},
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password(self):
        pw = self.cleaned_data["password"]
        if len(pw) < 8 or not re.search(r"\d", pw):
            raise forms.ValidationError("Use at least 8 characters, including a number.")
        return pw

    def clean(self):
        data = super().clean()
        if data.get("password") and data.get("confirm_password") and data["password"] != data["confirm_password"]:
            self.add_error("confirm_password", "Passwords don't match.")
        return data

    def save(self):
        d = self.cleaned_data
        first, _, last = d["full_name"].strip().partition(" ")
        return User.objects.create_user(
            username=d["email"], email=d["email"], password=d["password"],
            first_name=first, last_name=last,
        )
