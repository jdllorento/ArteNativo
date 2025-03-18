from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirigir al dashboard según el rol
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