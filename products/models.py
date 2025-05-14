from django.db import models
from django.conf import settings
from django.db.models import Avg
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
    image = models.ImageField(
        upload_to='products/', blank=True, null=True, default='products/default.jpg')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products")
    date_added = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        avg = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 1) if avg else 0

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        'products.Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating} Stars"
