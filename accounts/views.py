from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, RegistrationForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        # Allow email login as well.
        if user is None:
            try:
                account = User.objects.get(email__iexact=username)
                user = authenticate(
                    request,
                    username=account.username,
                    password=password,
                )
            except User.DoesNotExist:
                user = None

        if user is not None:

            if not user.is_active:
                messages.error(
                    request,
                    "Your account is inactive."
                )
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form},
                )

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.first_name or user.username}!"
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username/email or password."
        )

    return render(
        request,
        "accounts/login.html",
        {"form": form},
    )


def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        user = form.save(commit=False)

        # Public registration always creates a citizen.
        user.role = User.Role.CITIZEN
        user.is_demo_user = False

        user.save()

        messages.success(
            request,
            "Registration successful. You can now login."
        )

        return redirect("login")

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("home")

@login_required
def dashboard(request):

    role = request.user.role

    if role == User.Role.CITIZEN:
        return redirect("citizens:citizen_dashboard")

    if role == User.Role.OFFICER:
        return redirect("officer_dashboard")

    if role == User.Role.SYSTEM_ADMIN:
        return redirect("admin_dashboard")

    if role == User.Role.API_ADMIN:
        return redirect("integration_dashboard")

    messages.error(
        request,
        "Your account does not have a valid role."
    )

    return redirect("home")

def home(request):
    return render(request, "public/home.html")

def about(request):
    return render(request, "public/about.html")