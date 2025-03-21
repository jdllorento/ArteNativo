from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import BasicRegistrationForm, FullRegistrationForm


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "users/login.html", {"error": "Credenciales incorrectas"})

    return render(request, "users/login.html")


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request, "users/admin_dashboard.html")
    else:
        return render(request, "users/customer_dashboard.html")


def user_logout(request):
    logout(request)
    return redirect("login")


def basic_register(request):
    """
    Registro básico: solo username y password.
    """
    if request.method == 'POST':
        form = BasicRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = user.CUSTOMER
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = BasicRegistrationForm()
    return render(request, 'users/basic_register.html', {'form': form})


@login_required
def full_register(request):
    user = request.user

    if request.method == 'POST':
        form = FullRegistrationForm(
            request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = FullRegistrationForm(instance=user)

    return render(request, 'users/full_register.html', {'form': form})
