from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CouponApplyForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    """
    Validates the coupon and stores it's ID in a user's session
    """
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
        messages.success(request, "Coupon code applied.")
    return redirect("cart:cart_detail")


@require_POST
def coupon_remove(request):
    pass
