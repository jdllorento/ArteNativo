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

    def is_admin(self):
        return self.role == self.ADMIN

    def is_customer(self):
        return self.role == self.CUSTOMER

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Customer(User):
    address = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"