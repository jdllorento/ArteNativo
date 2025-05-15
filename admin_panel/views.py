from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.utils.translation import gettext_lazy as _
# Create your views here.


@login_required
def add_product(request):
    if not request.user.is_staff:
        return redirect('product_list')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('product_list')

    else:
        form = ProductForm()

    return render(request, 'admin_panel/add_product.html', {'form': form})
