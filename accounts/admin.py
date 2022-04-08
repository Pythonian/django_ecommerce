from django.contrib import admin
from django.core.mail import send_mail

from .models import Customer, Vendor, User


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # list_display = ['user', 'phone_number', 'address', 'postal_code', 'city']
    pass


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['user']

    def save_model(self, request, obj, form, change):
        if obj.is_verified is True:
            send_mail(
                'Congratulations! Verification Approved',
                'You are now a verified seller on our platform and you can now start selling.',
                'from@example.com',
                [obj.user.email],
                fail_silently=False)
        super(VendorAdmin, self).save_model(request, obj, form, change)
    

admin.site.register(User)
