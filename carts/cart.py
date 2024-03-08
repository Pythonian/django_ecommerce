from decimal import Decimal

from products.models import Product
from coupons.models import Coupon

CART_SESSION_ID = "cart"


class Cart:
    """Manage shopping cart."""

    def __init__(self, request):
        """Initialize the cart with a request object."""
        # store the current session
        self.session = request.session
        # try to get the cart from the current session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get("coupon_id")

    def __iter__(self):
        """Iterate over the items in the cart and get the products from the db."""
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        # copy the current cart in the cart variable
        cart = self.cart.copy()
        # add the product instances to the cart
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            # convert each item price back to decimal
            item["price"] = Decimal(item["price"])
            # adds a total price attribute to each item
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Return the total number of items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        params:
            product:  The product instance to add or update in the cart.
            quantity: An optional integer with the product quantity.
            override_quantity: A Boolean that indicates whether the quantity
              needs to be overridden with the given quantity (True), or if the
              new quantity has to be added to the existing quantity (False).
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        # mark the session as modified to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """return the total cost of the items in the cart."""
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self):
        """Remove cart from user session"""
        del self.session[CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """Return the Coupon object with the given ID if cart contains a coupon_id."""
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """
        Retrieve discount rate and return the amount to be deducted
        from the total amount of the cart.
        """
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        """Return the total amount of the cart after deducting the amount
        returned by the get_discount() method."""
        return self.get_total_price() - self.get_discount()
