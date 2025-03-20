from django.urls import path
from .views import product_list, product_detail, add_review

urlpatterns = [
    path('', product_list, name = 'product_list'),
    path('<int:product_id>/', product_detail, name = 'product_detail'),
    path('<int:product_id>/add-review/', add_review, name = 'add_review')
]