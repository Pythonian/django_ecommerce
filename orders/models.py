from datetime import datetime, timedelta
from django.db import models

from accounts.models import User, Vendor
from products.models import Product


class Order(models.Model):
    CREATED = 'Created'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    COMPLETED = 'Completed'
    # CANCELLED = 'Cancelled'
    # RETURNED = 'Returned'
    ORDER_STATUS = [
        (CREATED, 'Created'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (COMPLETED, 'Completed'),
        # (CANCELLED, 'Cancelled'),
        # (RETURNED, 'Returned'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders',
        blank=True, null=True) # models.SET_NULL
    # full_name?
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    # address1 / address2?
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(
        choices=ORDER_STATUS, max_length=10, default=CREATED)
    note = models.TextField(blank=True)
    delivery_date = models.DateTimeField(default=datetime.now()+timedelta(days=4))
    # transaction_id = models.CharField(max_length=200, blank=True, null=True)
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        blank=True, null=True)
    paystack_id = models.CharField(max_length=150, blank=True)
    vendors = models.ManyToManyField(Vendor, related_name='orders')

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='orderitems',
        blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, related_name='items',
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # vendor_paid = models.BooleanField(default=False)
    # status?

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
