# from django.db import models
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     image = models.ImageField(upload_to='categories/', blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Product(models.Model):
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         related_name='products'
#     )
#
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()
#
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )
#
#     # Admin sirf discount percentage dalega
#     discount_percentage = models.PositiveIntegerField(
#         default=0,
#         help_text="Enter discount percentage (Example: 10 for 10%)"
#     )
#
#     stock = models.PositiveIntegerField(default=0)
#
#     image = models.ImageField(
#         upload_to='products/'
#     )
#
#     available = models.BooleanField(default=True)
#
#     created = models.DateTimeField(
#         auto_now_add=True
#     )
#
#     class Meta:
#         ordering = ['-created']
#
#     @property
#     def discounted_price(self):
#         if self.discount_percentage > 0:
#             discount_amount = (self.price * self.discount_percentage) / 100
#             return round(self.price - discount_amount, 2)
#         return self.price
#
#     def __str__(self):
#         return self.name

# from django.db import models
#
#
# # =========================
# # CATEGORY MODEL
# # =========================
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
#     image = models.ImageField(upload_to='categories/', blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# # =========================
# # PRODUCT MODEL (UPDATED)
# # =========================
# class Product(models.Model):
#
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         related_name='products'
#     )
#
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()
#
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )
#
#     # Discount percentage (admin input)
#     discount_percentage = models.PositiveIntegerField(
#         default=0,
#         help_text="Enter discount percentage (Example: 10 for 10%)"
#     )
#
#     # Total stock (overall)
#     stock = models.PositiveIntegerField(default=0)
#
#     # =========================
#     # SIZE SUPPORT (NEW ADDITION)
#     # =========================
#     SIZE_CHOICES = (
#         ('S', 'Small'),
#         ('M', 'Medium'),
#         ('L', 'Large'),
#         ('XL', 'Extra Large'),
#     )
#
#     size_available = models.CharField(
#         max_length=10,
#         choices=SIZE_CHOICES,
#         default='M'
#     )
#
#     image = models.ImageField(upload_to='products/')
#
#     available = models.BooleanField(default=True)
#
#     created = models.DateTimeField(auto_now_add=True)
#
#     # =========================
#     # META
#     # =========================
#     class Meta:
#         ordering = ['-created']
#
#     # =========================
#     # DISCOUNT PRICE LOGIC
#     # =========================
#     @property
#     def discounted_price(self):
#         if self.discount_percentage > 0:
#             discount_amount = (self.price * self.discount_percentage) / 100
#             return round(self.price - discount_amount, 2)
#         return self.price
#
#     def __str__(self):
#         return self.name

# from django.db import models
# from django.contrib.auth.models import User
# from cloudinary.models import CloudinaryField
# # =========================
# # CATEGORY MODEL
# # =========================
# class Category(models.Model):
#
#     name = models.CharField(
#         max_length=100
#     )
#
#     slug = models.SlugField(
#         unique=True
#     )
#
#     # image = models.ImageField(
#     #     upload_to='categories/',
#     #     blank=True,
#     #     null=True
#     # )
#     # image = CloudinaryField('image', blank=True, null=True)
#     image = CloudinaryField(
#         'image',
#         folder='categories',
#         blank=True,
#         null=True
#     )
#
#     def __str__(self):
#         return self.name
#
#
# # =========================
# # PRODUCT MODEL
# # =========================
# class Product(models.Model):
#
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE,
#         related_name='products'
#     )
#
#     name = models.CharField(
#         max_length=200
#     )
#
#     slug = models.SlugField(
#         unique=True
#     )
#
#     description = models.TextField()
#
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )
#
#     # =========================
#     # DISCOUNT
#     # =========================
#     discount_percentage = models.PositiveIntegerField(
#         default=0,
#         help_text="Enter discount percentage (Example: 10 for 10%)"
#     )
#
#     # =========================
#     # TOTAL STOCK
#     # =========================
#     stock = models.PositiveIntegerField(
#         default=0
#     )
#
#     # =========================
#     # MULTIPLE SIZE SUPPORT
#     # =========================
#     sizes = models.CharField(
#         max_length=100,
#         default='M',
#         help_text="Example: S,M,L,XL"
#     )
#
#     # image = models.ImageField(
#     #     upload_to='products/'
#     # )
#     image = CloudinaryField('image', folder='products')
#
#     available = models.BooleanField(
#         default=True
#     )
#
#     created = models.DateTimeField(
#         auto_now_add=True
#     )
#
#     # =========================
#     # META
#     # =========================
#     class Meta:
#         ordering = ['-created']
#
#     # =========================
#     # DISCOUNTED PRICE
#     # =========================
#     @property
#     def discounted_price(self):
#
#         if self.discount_percentage > 0:
#
#             discount_amount = (
#                 self.price * self.discount_percentage
#             ) / 100
#
#             return round(
#                 self.price - discount_amount,
#                 2
#             )
#
#         return self.price
#
#     # =========================
#     # SIZE LIST
#     # =========================
#     def get_sizes_list(self):
#
#         return [
#             size.strip()
#             for size in self.sizes.split(',')
#             if size.strip()
#         ]
#
#     def __str__(self):
#         return self.name
#
# class ProductReview(models.Model):
#
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='reviews'
#     )
#
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE
#     )
#
#     rating = models.PositiveIntegerField(default=5)
#
#     comment = models.TextField()
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} - {self.product.name}"
#
# class Wishlist(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='wishlist_items'
#     )
#
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='wishlisted_by'
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('user', 'product')
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"{self.user.username} - {self.product.name}"

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# =========================
# CATEGORY MODEL
# =========================
class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    slug = models.SlugField(
        unique=True
    )

    image = CloudinaryField(
        'image',
        folder='categories',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# =========================
# PRODUCT MODEL
# =========================
class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # DISCOUNT
    discount_percentage = models.PositiveIntegerField(
        default=0,
        help_text="Enter discount percentage (Example: 10 for 10%)"
    )

    # STOCK
    stock = models.PositiveIntegerField(
        default=0
    )

    # MULTIPLE SIZES
    sizes = models.CharField(
        max_length=100,
        default='M',
        help_text="Example: S,M,L,XL"
    )

    # MAIN IMAGE
    image = CloudinaryField(
        'image',
        folder='products'
    )

    available = models.BooleanField(
        default=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created']

    # DISCOUNTED PRICE
    @property
    def discounted_price(self):

        if self.discount_percentage > 0:

            discount_amount = (
                self.price * self.discount_percentage
            ) / 100

            return round(
                self.price - discount_amount,
                2
            )

        return self.price

    # SIZE LIST
    def get_sizes_list(self):

        return [
            size.strip()
            for size in self.sizes.split(',')
            if size.strip()
        ]

    def __str__(self):
        return self.name


# =========================
# MULTIPLE PRODUCT IMAGES
# =========================
class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images'
    )

    image = CloudinaryField(
        'image',
        folder='product_gallery'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.name} Gallery Image"


# =========================
# PRODUCT REVIEW
# =========================
class ProductReview(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.PositiveIntegerField(
        default=5
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


# =========================
# WISHLIST
# =========================
class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist_items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"