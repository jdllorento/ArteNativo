from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from .serializers import ProductsSerializer
import google.generativeai as genai
from .datasources import DatabaseProductDataSource, HardcodedProductDataSource, IProductDataSource
# Create your views here.

genai.configure(api_key="aquivalaapikey")
model = genai.GenerativeModel('gemini-2.0-flash')


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

    review_text = [reviews for review in reviews]

    review_overview = ""

    if review_text:
        prompt = f"""Here are some reviews for the product {product.name}:\n\n"""
        prompt += "\n".join(f"- {text}" for text in review_text)
        prompt += f"\n\nGenerate a concise overview in spanish of what customers are saying about the product in these reviews. Highlight the main positive and negative points. Dont mention the customers or the rating specifically just say if it is positive, negative or mixed."
        try:
            response = model.generate_content(prompt)
            review_overview = response.text
        except Exception as e:
            review_overview = "Error generating overview: " + str(e)
            print(review_overview)
    else:
        review_overview = "No hay reseñas disponibles para este producto."

    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews, 'average_rating': average_rating, 'review_overview': review_overview})


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
