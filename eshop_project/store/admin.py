# from django.contrib import admin
# # from .models import Category, Product
# #
# # admin.site.register(Category)
# # admin.site.register(Product)
#
# from .models import Category, Product
# from django.contrib import admin
# from .models import Category, Product, ProductReview, Wishlist
#
#
# # =========================
# # WISHLIST ADMIN
# # =========================
# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#
#     list_display = (
#         'user',
#         'product',
#         'created_at'
#     )
#
#     search_fields = (
#         'user__username',
#         'product__name'
#     )
#
#     list_filter = (
#         'created_at',
#     )
#
#
# # =========================
# # CATEGORY ADMIN
# # =========================
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#
#     list_display = (
#         'name',
#         'slug'
#     )
#
#     prepopulated_fields = {
#         'slug': ('name',)
#     }
#
#
# # =========================
# # PRODUCT ADMIN
# # =========================
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#
#     list_display = (
#         'name',
#         'category',
#         'price',
#         'discount_percentage',
#         'discounted_price',
#         'stock',
#         'available',
#         'created'
#     )
#
#     list_filter = (
#         'available',
#         'category',
#         'created'
#     )
#
#     search_fields = (
#         'name',
#         'description'
#     )
#
#     prepopulated_fields = {
#         'slug': ('name',)
#     }
#
#
# # =========================
# # PRODUCT REVIEW ADMIN
# # =========================
# @admin.register(ProductReview)
# class ProductReviewAdmin(admin.ModelAdmin):
#
#     list_display = (
#         'product',
#         'user',
#         'rating',
#         'created_at'
#     )
#
#     list_filter = (
#         'rating',
#         'created_at'
#     )
#
#     search_fields = (
#         'product__name',
#         'user__username',
#         'comment'
#     )


from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductReview,
    Wishlist,
    ProductImage
)


# =========================
# PRODUCT GALLERY INLINE
# =========================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4
    fields = ['image']


# =========================
# WISHLIST ADMIN
# =========================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'product',
        'created_at'
    )

    search_fields = (
        'user__username',
        'product__name'
    )

    list_filter = (
        'created_at',
    )


# =========================
# CATEGORY ADMIN
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'slug'
    )

    prepopulated_fields = {
        'slug': ('name',)
    }


# =========================
# PRODUCT ADMIN
# =========================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'price',
        'discount_percentage',
        'discounted_price',
        'stock',
        'available',
        'created'
    )

    list_filter = (
        'available',
        'category',
        'created'
    )

    search_fields = (
        'name',
        'description'
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

    # MULTIPLE IMAGES INLINE
    inlines = [ProductImageInline]


# =========================
# PRODUCT REVIEW ADMIN
# =========================
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):

    list_display = (
        'product',
        'user',
        'rating',
        'created_at'
    )

    list_filter = (
        'rating',
        'created_at'
    )

    search_fields = (
        'product__name',
        'user__username',
        'comment'
    )


# =========================
# PRODUCT GALLERY ADMIN
# =========================
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = (
        'product',
        'created_at'
    )

    search_fields = (
        'product__name',
    )