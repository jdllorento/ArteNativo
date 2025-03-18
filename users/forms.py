from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

DOCUMENT_TYPES = [
    ('CC', 'Cédula de Ciudadanía'),
    ('TI', 'Tarjeta de Identidad'),
    ('CE', 'Cédula de Extranjería'),
    ('PP', 'Pasaporte'),
]

class BasicRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        # Se requieren solo username y password
        fields = ['username', 'password1', 'password2']

class FullRegistrationForm(UserCreationForm):
    # Campos adicionales para el registro completo
    first_name = forms.CharField(max_length=150, required=True, label="Nombre")
    last_name = forms.CharField(max_length=150, required=True, label="Apellido")
    email = forms.EmailField(required=True, label="Correo electrónico")
    address = forms.CharField(widget=forms.Textarea, required=True, label="Dirección")
    document_type = forms.ChoiceField(choices=DOCUMENT_TYPES, required=True ,label="Tipo de documento")
    document_number = forms.CharField(max_length=20, required=True, label="Número de documento")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'document_type', 'document_number','password1', 'password2',]
