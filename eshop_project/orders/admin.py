# # UPDATED orders/admin.py
#
# from django.contrib import admin
# from .models import Order, OrderItem, ShippingAddress
#
#
# @admin.register(ShippingAddress)
# class ShippingAddressAdmin(admin.ModelAdmin):
#     list_display = ['user', 'full_name', 'city', 'state', 'pincode']
#     search_fields = ['user__username', 'full_name', 'city']
#
#
# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'user',
#         'ordered_date',
#         'status',
#         'total_amount',
#         'payment_method'
#     ]
#
#     list_filter = [
#         'status',
#         'payment_method',
#         'ordered_date'
#     ]
#
#     search_fields = [
#         'user__username',
#         'id'
#     ]
#
#     inlines = [OrderItemInline]
# from .models import Coupon
# admin.site.register(Coupon)

from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    ShippingAddress,
    Coupon,
)


# =========================
# SHIPPING ADDRESS ADMIN
# =========================
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'full_name',
        'phone',
        'city',
        'state',
        'pincode',
        'created_at'
    ]

    search_fields = [
        'user__username',
        'full_name',
        'phone',
        'city',
        'state',
        'pincode'
    ]

    list_filter = [
        'state',
        'city',
        'created_at'
    ]


# =========================
# ORDER ITEM INLINE
# =========================
class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0

    readonly_fields = [
        'product',
        'quantity',
        'price'
    ]


# =========================
# ORDER ADMIN
# =========================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'user',
        'shipping_address',
        'ordered_date',
        'status',
        'total_amount',
        'payment_method',
        'complete'
    ]

    list_filter = [
        'status',
        'payment_method',
        'complete',
        'ordered_date'
    ]

    search_fields = [
        'user__username',
        'id',
        'shipping_address__full_name',
        'shipping_address__phone'
    ]

    readonly_fields = [
        'ordered_date',
        'total_amount'
    ]

    inlines = [
        OrderItemInline
    ]


# =========================
# COUPON ADMIN
# =========================
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = [
        'code',
        'discount_percentage',
        'active',
        'valid_from',
        'valid_to'
    ]

    list_filter = [
        'active',
        'valid_from',
        'valid_to'
    ]

    search_fields = [
        'code'
    ]