from django.db import models
from django.conf import settings
from cart.models import Cart

# Create your models here.
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=[('card', 'Tarjeta'), ('paypal', 'PayPal'), ('bank', 'Transferencia Bancaria')])
    created_at = models.DateTimeField(auto_now_add=True)

    def total(self):
        return self.cart.subtotal()

    def __str__(self):
        return f"Orden {self.id} - Usuario: {self.user.username}"