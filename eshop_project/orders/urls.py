# # =========================
# # orders/urls.py
# # =========================
#
# from django.urls import path
# from . import views
#
#
# urlpatterns = [
#     path(
#         'cart/',
#         views.cart_view,
#         name='cart'
#     ),
#
#     path(
#         'add-to-cart/<int:product_id>/',
#         views.add_to_cart,
#         name='add_to_cart'
#     ),
#
#     path(
#         'update-cart/<int:product_id>/<str:action>/',
#         views.update_cart,
#         name='update_cart'
#     ),
#
#     path(
#         'remove-from-cart/<int:product_id>/',
#         views.remove_from_cart,
#         name='remove_from_cart'
#     ),
#
#     path(
#         'checkout/',
#         views.checkout_view,
#         name='checkout'
#     ),
#
#     path(
#         'order-success/',
#         views.order_success_view,
#         name='order_success'
#     ),
#
#     path(
#         'my-orders/',
#         views.my_orders_view,
#         name='my_orders'
#     ),
# ]

from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # CART VIEW
    # =========================
    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),

    # =========================
    # ADD TO CART (SIZE FIX)
    # =========================
    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    # =========================
    # UPDATE CART (NOW NEED SIZE)
    # =========================
    path(
        'update-cart/<int:product_id>/<str:size>/<str:action>/',
        views.update_cart,
        name='update_cart'
    ),

    # =========================
    # REMOVE FROM CART (SIZE FIX)
    # =========================
    path(
        'remove-from-cart/<int:product_id>/<str:size>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    # =========================
    # CHECKOUT
    # =========================
    path(
        'checkout/',
        views.checkout_view,
        name='checkout'
    ),

    # =========================
    # SUCCESS PAGE
    # =========================
    path(
        'order-success/',
        views.order_success_view,
        name='order_success'
    ),

    # =========================
    # MY ORDERS
    # =========================
    path(
        'my-orders/',
        views.my_orders_view,
        name='my_orders'
    ),
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'update-order-status/<int:order_id>/<str:status>/',
        views.update_order_status,
        name='update_order_status'
    ),
    # path('my-orders/', views.my_orders, name='my_orders'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('payment/', views.payment_view, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    # path(
    #     'update-order-status/<int:order_id>/<str:status>/',
    #     views.update_order_status,
    #     name='update_order_status'
    # ),
]