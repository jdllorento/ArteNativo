from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = "admin"
    CUSTOMER = "customer"

    ROLE_CHOICES = [
        (ADMIN, "Administrador"),
        (CUSTOMER, "Cliente"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    address = models.TextField(blank=True, null=True)

    document_type = models.CharField(max_length=3, choices=[
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PP', 'Pasaporte'),
    ], blank=True, null=True)

    document_number = models.CharField(max_length=20, blank=True, null=True)

    def is_admin(self):
        return self.role == self.ADMIN

    def is_customer(self):
        return self.role == self.CUSTOMER

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Customer(User):
    #address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"