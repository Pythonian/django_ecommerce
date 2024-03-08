from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from coupons.forms import CouponApplyForm

from .cart import Cart
from .forms import CartAddProductForm


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(initial={"quantity": item["quantity"], "override": True})
    coupon_apply_form = CouponApplyForm()

    template = "cart/detail.html"
    context = {"cart": cart, "coupon_apply_form": coupon_apply_form}

    return render(request, template, context)


@require_POST
def cart_add(request, product_id):
    """
    View for adding products to the cart or updating quantities
    for existing products.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd["quantity"], override_quantity=cd["override"])
        # TODO: edit the message text based on override_quantity
        messages.success(request, "Shopping cart updated.")
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    """
    View to remove a product from cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, "Product removed from cart.")
    if cart:
        return redirect("cart:cart_detail")
    return redirect("/")
