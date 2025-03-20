from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True, default='products/default.jpg')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name