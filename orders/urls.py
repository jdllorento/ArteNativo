from django.urls import path
from .views import checkout, purchase_confirmation

urlpatterns = [
    path('', checkout, name='checkout'),
    path('confirmation/', purchase_confirmation, name='purchase_confirmation'),
]