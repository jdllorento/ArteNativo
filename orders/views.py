from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from .models import Order
from cart.models import Cart
from .utils import generate_pdf
from django.utils.translation import gettext_lazy as _
# Create your views here.


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    print("Carrito encontrado:", cart.id)  # Depuración

    if not request.user.has_complete_registration():
        return redirect('full_register')

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        print("Método de pago recibido:", payment_method)  # Depuración
        if payment_method:
            # Guardar el método de pago en la sesión
            request.session['payment_method'] = payment_method
            messages.success(request, _("Compra realizada con éxito."))
            return redirect('purchase_confirmation')

    return render(request, 'orders/checkout.html', {'cart': cart})


@login_required
def purchase_confirmation(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.items.count() == 0:
        messages.error(request, _("Tu carrito está vacío."))
        return redirect('cart_detail')

    payment_method = request.session.get('payment_method')
    total_paid = cart.total_price()

    cart_items = list(cart.items.all())

    pdf_buffer = generate_pdf(cart_items, total_paid,
                              payment_method, request.user)

    cart.items.all().delete()

    messages.success(
        request, _("Compra realizada con éxito. Tu carrito ha sido vaciado."))

    response = render(request, 'orders/purchase_confirmation.html',
                      {'cart': cart, 'payment_method': payment_method, 'total_paid': total_paid, 'cart_items': cart_items})

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura.pdf"'

    return response
