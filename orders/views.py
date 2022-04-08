from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from carts.cart import Cart

from .models import OrderItem, Order
from .forms import OrderCreateForm


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            for item in cart:
                if request.user.is_authenticated:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        user=request.user,
                        vendor=item['product'].vendor.vendor,
                        quantity=item['quantity'])
                    order.vendors.add(item['product'].vendor.vendor)
                else:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        vendor=item['product'].vendor.vendor,
                        quantity=item['quantity'])
                    order.vendors.add(item['product'].vendor)

            # clear the cart
            cart.clear()
            return render(request,
                          'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'address': request.user.customer.address,
                'phone_number': request.user.customer.phone_number,
                'postal_code': request.user.customer.postal_code,
                'city': request.user.customer.city,
            }
            form = OrderCreateForm(initial=initial_data)
    return render(request,
                  'orders/create.html',
                  {'cart': cart, 'form': form})


@login_required
def track_order(request, id):
    order = get_object_or_404(Order, id=id)

    return render(
        request, 'orders/track_order.html', {'order': order})


@login_required
def order_status_shipped(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.SHIPPED
    order.save()
    messages.success(
        request, "Order status changed to: Shipped")
    return redirect(current_url)


@login_required
def order_status_processing(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.PROCESSING
    order.save()
    messages.success(
        request, "Order status changed to: Processing")
    return redirect(current_url)


@login_required
def order_status_completed(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.COMPLETED
    order.save()
    messages.success(
        request, "Order status changed to: Completed")
    return redirect(current_url)
