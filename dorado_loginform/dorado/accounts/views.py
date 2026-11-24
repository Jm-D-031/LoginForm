from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


class DoradoLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        # "Remember me" unchecked -> session ends when the browser closes.
        if not form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)
        return response


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user, backend="accounts.backends.EmailBackend")
        return redirect("home")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def home(request):
    return render(request, "home.html")
