from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from paystack.api.signals import payment_verified

from .models import Order

@receiver(payment_verified)
def on_payment_verified(sender, ref, amount, order, **kwargs):
    get_order = get_object_or_404(Order, paystack_id=order)
    get_order.paid = True
    get_order.save()