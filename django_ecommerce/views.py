from django.http import JsonResponse
from django.shortcuts import render

from products.models import Product


def home(request):
    products = Product.objects.filter(is_approved=True)[:12]
    featured = Product.objects.filter(featured=True, is_approved=True)

    template_name = "home.html"
    context = {
        "products": products,
        "featured_products": featured,
    }

    return render(request, template_name, context)


def update_cart(request):
    return JsonResponse("Item was added", safe=False)
