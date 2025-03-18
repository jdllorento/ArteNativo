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

def basic_register(request):
    """
    Registro básico: solo username y password.
    """
    if request.method == 'POST':
        form = BasicRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Establecer el rol a "cliente" (ajusta según tu implementación)
            user.role = user.CUSTOMER  
            user.save()
            login(request, user)
            return redirect('dashboard')  # Redirige al dashboard u otra página
    else:
        form = BasicRegistrationForm()
    return render(request, 'users/basic_register.html', {'form': form})

def full_register(request):
    """
    Registro completo: solicita datos adicionales.
    """
    if request.method == 'POST':
        form = FullRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = user.CUSTOMER  # Establecer rol de cliente
            # Los campos first_name, last_name y email se asignan automáticamente al usar UserCreationForm
            # Guardamos el usuario; para el campo 'address' podrías guardarlo en un perfil extendido o en el modelo Customer
            user.save()
            # Si usas un modelo Customer, podrías crear una instancia de Customer aquí, por ejemplo:
            # Customer.objects.create(user=user, address=form.cleaned_data.get('address'))
            login(request, user)
            return redirect('dashboard')
    else:
        form = FullRegistrationForm()
    return render(request, 'users/full_register.html', {'form': form})