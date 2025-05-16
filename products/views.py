from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from .serializers import ProductsSerializer
from .datasources import DatabaseProductDataSource, HardcodedProductDataSource, IProductDataSource
# Create your views here.


def product_list(request):
    order = request.GET.get('order', 'default')
    category_id = request.GET.get('category', None)
    categories = Category.objects.all()

    products = Product.objects.annotate(average_rating=Avg('reviews__rating'))

    if category_id:
        products = products.filter(category_id=category_id)

    if order == 'rating':
        products = products.order_by('-average_rating')

    return render(request, 'products/product_list.html', {'products': products, 'order': order, 'categories': categories, 'selected_category': category_id})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    average_rating = Avg('reviews__rating')
    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews, 'average_rating': average_rating})


def serialize_products(request):
    source_type = request.GET.get('source', 'db')
    
    product_data_source: IProductDataSource
    if source_type == 'hardcoded':
        product_data_source = HardcodedProductDataSource()
    else:
        product_data_source = DatabaseProductDataSource()

    products = product_data_source.get_products()
    
    serializer = ProductsSerializer(products, many=True)
    return JsonResponse({'Products Available': serializer.data})


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'products/add_review.html', {'form': form, 'product': product})
