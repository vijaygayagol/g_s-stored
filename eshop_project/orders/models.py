# # orders/models.py
#
# from django.db import models
# from django.contrib.auth.models import User
# from store.models import Product
#
#
# # =========================
# # SHIPPING ADDRESS
# # =========================
# class ShippingAddress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=200)
#     phone = models.CharField(max_length=15)
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.city}"
#
#
# # =========================
# # ORDER
# # =========================
# class Order(models.Model):
#     ORDER_STATUS = (
#         ('Pending', 'Pending'),
#         ('Processing', 'Processing'),
#         ('Shipped', 'Shipped'),
#         ('Delivered', 'Delivered'),
#         ('Cancelled', 'Cancelled'),
#     )
#
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     shipping_address = models.ForeignKey(
#         ShippingAddress,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#
#     ordered_date = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False)
#
#     status = models.CharField(
#         max_length=20,
#         choices=ORDER_STATUS,
#         default='Pending'
#     )
#
#     total_amount = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         default=0
#     )
#
#     payment_method = models.CharField(
#         max_length=50,
#         default='Cash on Delivery'
#     )
#
#     def __str__(self):
#         return f"Order #{self.id}"
#
#
# # =========================
# # ORDER ITEM
# # =========================
# class OrderItem(models.Model):
#     order = models.ForeignKey(
#         Order,
#         on_delete=models.CASCADE,
#         related_name='items'
#     )
#
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#
#     quantity = models.PositiveIntegerField(default=1)
#
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )
#
#     def subtotal(self):
#         return self.quantity * self.price
#
#     def __str__(self):
#         return f"{self.product.name} ({self.quantity})"

# orders/models.py

from django.db import models
from django.contrib.auth.models import User
from store.models import Product


# =========================
# SHIPPING ADDRESS
# =========================
class ShippingAddress(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(
        max_length=200
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.city}"


# =========================
# ORDER
# =========================
class Order(models.Model):

    ORDER_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ordered_date = models.DateTimeField(
        auto_now_add=True
    )

    complete = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='Pending'
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=50,
        default='Cash on Delivery'
    )

    # =========================
    # ADMIN FEATURES
    # =========================
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    delivery_date = models.DateTimeField(
        blank=True,
        null=True
    )

    admin_note = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Order #{self.id}"

    # =========================
    # STATUS HELPERS
    # =========================
    @property
    def is_pending(self):
        return self.status == 'Pending'

    @property
    def is_processing(self):
        return self.status == 'Processing'

    @property
    def is_shipped(self):
        return self.status == 'Shipped'

    @property
    def is_delivered(self):
        return self.status == 'Delivered'

    @property
    def is_cancelled(self):
        return self.status == 'Cancelled'


# =========================
# ORDER ITEM
# =========================
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    # SELECTED SIZE
    size = models.CharField(
        max_length=10,
        default='M'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_percentage = models.PositiveIntegerField(
        help_text="Example: 10 for 10% off"
    )

    active = models.BooleanField(
        default=True
    )

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code