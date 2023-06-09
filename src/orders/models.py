from django.db import models
from shop.models import Product
from coupons.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    email = models.EmailField(_("Email"))
    address = models.CharField(_("address"), max_length=250)
    postal_code = models.CharField(_("Postal code"), max_length=20)
    city = models.CharField(_("City"), max_length=100)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    paid = models.BooleanField(_("Paid"), default=False)
    braintree_id = models.CharField(max_length=150, blank=True)

    coupon = models.ForeignKey(
        Coupon, related_name="orders", null=True, blank=True, on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        # Calculate and minus the discount from the total cost (if any)
        return total_cost - total_cost * (self.discount / Decimal(100))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "orders"

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
