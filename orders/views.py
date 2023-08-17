from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.conf import settings

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
            request.session['order_id'] = order.id

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
                    order.vendors.add(item['product'].vendor.vendor)

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
def confirm_order(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(order, id=order_id)

    paystack_amount = int(order.get_total_cost * 100)
    paystack_ref = None
    if not paystack_ref:
        paystack_ref = get_random_string(length=12).upper()
        order.paystack_id = paystack_ref
        order.total_amount = order.get_total_cost
        order.save()
    paystack_redirect_url = "{}?amount={}".format(
        reverse('paystack:verify_payment',
                args=[paystack_ref]), paystack_amount, order)

    template = 'orders/confirm_order.html'
    context = {'order': order,
                   'paystack_key': settings.PAYSTACK_PUBLIC_KEY,
                   'paystack_amount': paystack_amount,
                   'paystack_redirect_url': paystack_redirect_url
    }
    return render(request, template, context)


@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(order, id=order_id)
    return render(request, 'orders/invoice.html', {'order': order})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'orders/canceled.html')


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
    # send mail to user to inform him/her of change in order status
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email
    send_mail(
        'Order status information',
        'Hi there, your order status has been changed to: SHIPPED',
        from_email,
        [to_email],
        fail_silently=False
    )
    messages.success(
        request, "Order status changed to: Shipped")
    return redirect(current_url)


@login_required
def order_status_processing(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.PROCESSING
    order.save()
    # send mail to user to inform him/her of change in order status
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email
    send_mail(
        'Order status information',
        'Hi there, your order status has been changed to: PROCESSING',
        from_email,
        [to_email],
        fail_silently=False
    )
    messages.success(
        request, "Order status changed to: Processing")
    return redirect(current_url)


@login_required
def order_status_completed(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.COMPLETED
    order.save()
    # send mail to user to inform him/her of change in order status
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email
    send_mail(
        'Order status information',
        'Hi there, your order has successfully been completed.',
        from_email,
        [to_email],
        fail_silently=False
    )
    messages.success(
        request, "Order status changed to: Completed")
    return redirect(current_url)
