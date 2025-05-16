import requests
from django.shortcuts import render

headers = {
    'Accept': 'application/json',  # Specify that you want JSON
}

def product_list(request):
    # Fetch the JSON data
    url = "http://buy4u.3utilities.com:8000/api/products/"
    response = requests.get(url, headers=headers)
    products = response.json()  # Parse the JSON response

    # Pass the products to the template
    return render(request, "alied_products/product_list.html", {"products": products})