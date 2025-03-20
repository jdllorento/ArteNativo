from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Cart, CartItem
from products.models import Product

# Create your views here.

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        quantity = request.POST.get("quantity")

        if quantity and quantity.isdigit():
            quantity = int(quantity)

            if quantity < 1:
                quantity = 1
            elif quantity > product.stock:
                messages.error(request, f"Solo quedan {product.stock} unidades disponibles.")
                quantity = product.stock
            
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            
            cart_item.save()
            messages.success(request, "¡Producto agregado al carrito!")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('product_list')))

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})