# =========================
# orders/views.py
# =========================

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from store.models import Product
# from .models import Order, OrderItem
# from .forms import ShippingAddressForm
#
#
# def add_to_cart(request, product_id):
#
#     cart = request.session.get('cart', {})
#
#     product_id = str(product_id)
#
#     if product_id in cart:
#         cart[product_id] += 1
#     else:
#         cart[product_id] = 1
#
#     request.session['cart'] = cart
#     request.session.modified = True
#
#     return redirect('cart')
#
#
# @login_required(login_url='/login/')
# def cart_view(request):
#
#     cart = request.session.get('cart', {})
#
#     products = []
#     total = 0
#
#     for product_id, qty in cart.items():
#
#         try:
#             product = Product.objects.get(id=product_id)
#
#             product.qty = qty
#             product.total_price = float(product.discounted_price) * qty
#
#             total += product.total_price
#             products.append(product)
#
#         except Product.DoesNotExist:
#             continue
#
#     return render(request, 'orders/cart.html', {
#         'products': products,
#         'total': total
#     })
#
#
# def update_cart(request, product_id, action):
#
#     cart = request.session.get('cart', {})
#     product_id = str(product_id)
#
#     if product_id in cart:
#
#         if action == 'increase':
#             cart[product_id] += 1
#
#         elif action == 'decrease':
#             cart[product_id] -= 1
#
#             if cart[product_id] <= 0:
#                 del cart[product_id]
#
#     request.session['cart'] = cart
#     request.session.modified = True
#
#     return redirect('cart')
#
#
# def remove_from_cart(request, product_id):
#
#     cart = request.session.get('cart', {})
#     product_id = str(product_id)
#
#     if product_id in cart:
#         del cart[product_id]
#
#     request.session['cart'] = cart
#     request.session.modified = True
#
#     return redirect('cart')
#
#
# @login_required(login_url='/login/')
# def checkout_view(request):
#
#     cart = request.session.get('cart', {})
#
#     if not cart:
#         return redirect('product_list')
#
#     products = []
#     total = 0
#
#     for product_id, qty in cart.items():
#
#         product = get_object_or_404(
#             Product,
#             id=product_id
#         )
#
#         product.qty = qty
#         product.total_price = float(product.discounted_price) * qty
#
#         total += product.total_price
#         products.append(product)
#
#     form = ShippingAddressForm(
#         request.POST or None
#     )
#
#     if request.method == 'POST' and form.is_valid():
#
#         shipping = form.save(commit=False)
#         shipping.user = request.user
#         shipping.save()
#
#         order = Order.objects.create(
#             user=request.user,
#             shipping_address=shipping,
#             complete=True,
#             total_amount=total,
#             payment_method='Cash on Delivery'
#         )
#
#         for product in products:
#
#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=product.qty,
#                 price=product.discounted_price
#             )
#
#             product.stock -= product.qty
#             product.save()
#
#         request.session['cart'] = {}
#
#         return redirect('order_success')
#
#     return render(request, 'orders/checkout.html', {
#         'products': products,
#         'total': total,
#         'form': form,
#     })
#
#
# @login_required(login_url='/login/')
# def order_success_view(request):
#     return render(
#         request,
#         'orders/order_success.html'
#     )
#
#
# @login_required(login_url='/login/')
# def my_orders_view(request):
#
#     orders = Order.objects.filter(
#         user=request.user
#     ).order_by('-ordered_date')
#
#     return render(request, 'orders/my_orders.html', {
#         'orders': orders,
#     })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product
from .models import Order, OrderItem
from .forms import ShippingAddressForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .utils import send_order_sms
from django.utils import timezone
from .models import Coupon
import razorpay
from django.conf import settings
# =========================
# ADD TO CART (SIZE ADDED)
# =========================
def add_to_cart(request, product_id):

    size = request.POST.get('size', 'M')  # NEW

    cart = request.session.get('cart', {})

    key = f"{product_id}_{size}"  # IMPORTANT CHANGE

    if key in cart:
        cart[key]['qty'] += 1
    else:
        cart[key] = {
            'qty': 1,
            'size': size
        }

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# =========================
# CART VIEW
# =========================
# @login_required(login_url='/login/')
# def cart_view(request):
#
#     cart = request.session.get('cart', {})
#
#     products = []
#     total = 0
#
#     for key, item in cart.items():
#
#         try:
#             product_id = key.split('_')[0]
#             size = item['size']
#             qty = item['qty']
#
#             product = Product.objects.get(id=product_id)
#
#             product.qty = qty
#             product.size = size
#             product.available_stock = product.stock
#
#             product.total_price = float(product.discounted_price) * qty
#
#             total += product.total_price
#             products.append(product)
#
#         except Product.DoesNotExist:
#             continue
#
#     return render(request, 'orders/cart.html', {
#         'products': products,
#         'total': total
#     })

# @login_required(login_url='/login/')
# def cart_view(request):
#
#     cart = request.session.get('cart', {})
#
#     products = []
#     total = 0
#
#     for key, item in cart.items():
#
#         try:
#             product_id = key.split('_')[0]
#             product = Product.objects.get(id=product_id)
#
#             # =========================
#             # BACKWARD COMPATIBILITY FIX
#             # =========================
#
#             # OLD CART FORMAT (int qty)
#             if isinstance(item, int):
#                 qty = item
#                 size = 'M'   # default size
#
#             # NEW CART FORMAT (dict)
#             else:
#                 qty = item.get('qty', 1)
#                 size = item.get('size', 'M')
#
#             # attach dynamic fields
#             product.qty = qty
#             product.size = size
#             product.available_stock = product.stock
#
#             product.total_price = float(product.discounted_price) * qty
#
#             total += product.total_price
#             products.append(product)
#
#         except Product.DoesNotExist:
#             continue
#
#     return render(request, 'orders/cart.html', {
#         'products': products,
#         'total': total
#     })

@login_required(login_url='/login/')
def cart_view(request):

    cart = request.session.get('cart', {})

    products = []
    total = 0

    # =========================
    # CART PRODUCTS
    # =========================
    for key, item in cart.items():

        try:
            product_id = key.split('_')[0]

            product = Product.objects.get(
                id=product_id
            )

            # =========================
            # BACKWARD COMPATIBILITY
            # =========================

            # OLD CART FORMAT
            if isinstance(item, int):

                qty = item
                size = 'M'

            # NEW CART FORMAT
            else:

                qty = item.get(
                    'qty',
                    1
                )

                size = item.get(
                    'size',
                    'M'
                )

            # =========================
            # DYNAMIC PRODUCT DATA
            # =========================
            product.qty = qty
            product.size = size
            product.available_stock = product.stock

            product.total_price = (
                float(product.discounted_price)
                * qty
            )

            total += product.total_price

            products.append(product)

        except Product.DoesNotExist:
            continue

    # =========================
    # COUPON LOGIC
    # =========================
    coupon_discount = 0
    coupon = None

    coupon_id = request.session.get(
        'coupon_id'
    )

    if coupon_id:

        try:

            coupon = Coupon.objects.get(
                id=coupon_id,
                active=True
            )

            coupon_discount = (
                total
                * coupon.discount_percentage
            ) / 100

        except Coupon.DoesNotExist:

            request.session['coupon_id'] = None

    # =========================
    # FINAL TOTAL
    # =========================
    final_total = total - coupon_discount

    if final_total < 0:
        final_total = 0

    # =========================
    # RENDER
    # =========================
    return render(
        request,
        'orders/cart.html',
        {
            'products': products,
            'total': total,
            'coupon': coupon,
            'coupon_discount': coupon_discount,
            'final_total': final_total,
        }
    )
# =========================
# UPDATE CART (QTY +/-)
# =========================
# def update_cart(request, product_id, size, action):
#
#     cart = request.session.get('cart', {})
#
#     key = f"{product_id}_{size}"
#
#     if key in cart:
#
#         if action == 'increase':
#             cart[key]['qty'] += 1
#
#         elif action == 'decrease':
#             cart[key]['qty'] -= 1
#
#             if cart[key]['qty'] <= 0:
#                 del cart[key]
#
#     request.session['cart'] = cart
#     request.session.modified = True
#
#     return redirect('cart')
def update_cart(request, product_id, size, action):

    cart = request.session.get('cart', {})

    key = f"{product_id}_{size}"

    # =========================
    # OLD CART FORMAT SUPPORT
    # =========================
    if key not in cart and str(product_id) in cart:

        old_qty = cart[str(product_id)]

        # convert old cart -> new cart
        cart[key] = {
            'qty': old_qty,
            'size': size
        }

        del cart[str(product_id)]

    # =========================
    # UPDATE QUANTITY
    # =========================
    if key in cart:

        # SAFE CHECK
        if isinstance(cart[key], int):

            cart[key] = {
                'qty': cart[key],
                'size': size
            }

        # INCREASE
        if action == 'increase':
            cart[key]['qty'] += 1

        # DECREASE
        elif action == 'decrease':

            cart[key]['qty'] -= 1

            # REMOVE IF QTY <= 0
            if cart[key]['qty'] <= 0:
                del cart[key]

    # SAVE SESSION
    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

# =========================
# REMOVE FROM CART
# =========================
def remove_from_cart(request, product_id, size):

    cart = request.session.get('cart', {})

    key = f"{product_id}_{size}"

    if key in cart:
        del cart[key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# =========================
# CHECKOUT
# =========================
# @login_required(login_url='/login/')
# def checkout_view(request):
#
#     cart = request.session.get('cart', {})
#
#     if not cart:
#         return redirect('product_list')
#
#     products = []
#     total = 0
#
#     for key, item in cart.items():
#
#         product_id = key.split('_')[0]
#         size = item['size']
#         qty = item['qty']
#
#         product = get_object_or_404(Product, id=product_id)
#
#         # STOCK CHECK (IMPORTANT)
#         if qty > product.stock:
#             return redirect('cart')
#
#         product.qty = qty
#         product.size = size
#         product.total_price = float(product.discounted_price) * qty
#
#         total += product.total_price
#         products.append(product)
#
#     form = ShippingAddressForm(request.POST or None)
#
#     if request.method == 'POST' and form.is_valid():
#
#         shipping = form.save(commit=False)
#         shipping.user = request.user
#         shipping.save()
#
#         order = Order.objects.create(
#             user=request.user,
#             shipping_address=shipping,
#             complete=True,
#             total_amount=total,
#             payment_method='Cash on Delivery'
#         )
#
#         for product in products:
#
#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=product.qty,
#                 price=product.discounted_price
#             )
#
#             # STOCK REDUCE
#             product.stock -= product.qty
#             product.save()
#
#         # CLEAR CART
#         request.session['cart'] = {}
#         request.session.modified = True
#
#         return redirect('order_success')
#
#     return render(request, 'orders/checkout.html', {
#         'products': products,
#         'total': total,
#         'form': form,
#     })
# @login_required(login_url='/login/')
# def checkout_view(request):
#
#     cart = request.session.get('cart', {})
#
#     if not cart:
#         return redirect('product_list')
#
#     products = []
#     total = 0
#
#     for key, item in cart.items():
#
#         try:
#             product_id = key.split('_')[0]
#
#             # =========================
#             # OLD CART FORMAT SUPPORT
#             # =========================
#             if isinstance(item, int):
#
#                 qty = item
#                 size = 'M'
#
#             # =========================
#             # NEW CART FORMAT
#             # =========================
#             else:
#
#                 qty = item.get('qty', 1)
#                 size = item.get('size', 'M')
#
#             product = get_object_or_404(
#                 Product,
#                 id=product_id
#             )
#
#             # =========================
#             # STOCK CHECK
#             # =========================
#             if qty > product.stock:
#                 return redirect('cart')
#
#             # dynamic fields
#             product.qty = qty
#             product.size = size
#
#             product.total_price = (
#                 float(product.discounted_price) * qty
#             )
#
#             total += product.total_price
#             products.append(product)
#
#         except Exception as e:
#             print("Checkout Error:", e)
#             continue
#
#     form = ShippingAddressForm(
#         request.POST or None
#     )
#
#     # =========================
#     # PLACE ORDER
#     # =========================
#     if request.method == 'POST' and form.is_valid():
#
#         shipping = form.save(commit=False)
#         shipping.user = request.user
#         shipping.save()
#
#         order = Order.objects.create(
#             user=request.user,
#             shipping_address=shipping,
#             complete=True,
#             total_amount=total,
#             payment_method='Cash on Delivery'
#         )
#
#         # =========================
#         # SAVE ORDER ITEMS
#         # =========================
#         for product in products:
#
#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=product.qty,
#                 price=product.discounted_price
#             )
#
#             # reduce stock
#             product.stock -= product.qty
#             product.save()
#
#         # =========================
#         # CLEAR CART
#         # =========================
#         request.session['cart'] = {}
#         request.session.modified = True
#
#         return redirect('order_success')
#
#     return render(request, 'orders/checkout.html', {
#         'products': products,
#         'total': total,
#         'form': form,
#     })
# @login_required(login_url='/login/')
# def checkout_view(request):
#
#     cart = request.session.get('cart', {})
#
#     if not cart:
#         return redirect('product_list')
#
#     products = []
#     total = 0
#     stock_error = False
#
#     for key, item in cart.items():
#
#         try:
#             product_id = key.split('_')[0]
#
#             # =========================
#             # OLD CART FORMAT SUPPORT
#             # =========================
#             if isinstance(item, int):
#
#                 qty = item
#                 size = 'M'
#
#             else:
#
#                 qty = item.get('qty', 1)
#                 size = item.get('size', 'M')
#
#             product = get_object_or_404(
#                 Product,
#                 id=product_id
#             )
#
#             # =========================
#             # STOCK CHECK
#             # =========================
#             if product.stock <= 0:
#
#                 product.qty = qty
#                 product.size = size
#                 product.stock_error = "Out of Stock"
#
#                 stock_error = True
#
#             elif qty > product.stock:
#
#                 product.qty = qty
#                 product.size = size
#                 product.stock_error = f"Only {product.stock} left"
#
#                 stock_error = True
#
#             else:
#
#                 product.stock_error = None
#
#             product.total_price = (
#                 float(product.discounted_price) * qty
#             )
#
#             total += product.total_price
#             products.append(product)
#
#         except Exception as e:
#             print("Checkout Error:", e)
#             continue
#
#     form = ShippingAddressForm(
#         request.POST or None
#     )
#
#     # =========================
#     # STOP ORDER IF STOCK ISSUE
#     # =========================
#     if stock_error:
#         return render(request, 'orders/checkout.html', {
#             'products': products,
#             'total': total,
#             'form': form,
#             'stock_error': True,
#         })
#
#     # =========================
#     # PLACE ORDER
#     # =========================
#     if request.method == 'POST' and form.is_valid():
#
#         shipping = form.save(commit=False)
#         shipping.user = request.user
#         shipping.save()
#
#         order = Order.objects.create(
#             user=request.user,
#             shipping_address=shipping,
#             complete=True,
#             total_amount=total,
#             payment_method='Cash on Delivery'
#         )
#
#         for product in products:
#
#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=product.qty,
#                 price=product.discounted_price
#             )
#
#             product.stock -= product.qty
#             product.save()
#
#         request.session['cart'] = {}
#         request.session.modified = True
#
#         return redirect('order_success')
#
#     return render(request, 'orders/checkout.html', {
#         'products': products,
#         'total': total,
#         'form': form,
#     })

# @login_required(login_url='/login/')
# def checkout_view(request):
#
#     cart = request.session.get('cart', {})
#
#     if not cart:
#         return redirect('product_list')
#
#     products = []
#     total = 0
#
#     for key, item in cart.items():
#
#         try:
#             # OLD CART SUPPORT
#             if isinstance(item, int):
#                 product_id = key
#                 qty = item
#                 size = 'M'
#
#             else:
#                 product_id = key.split('_')[0]
#                 qty = item.get('qty', 1)
#                 size = item.get('size', 'M')
#
#             product = get_object_or_404(
#                 Product,
#                 id=product_id
#             )
#
#             # STOCK CHECK
#             if qty > product.stock or product.stock <= 0:
#                 return redirect('cart')
#
#             # DYNAMIC ATTRIBUTES
#             product.qty = qty
#             product.size = size
#             product.total_price = float(
#                 product.discounted_price
#             ) * qty
#
#             total += product.total_price
#             products.append(product)
#
#         except Product.DoesNotExist:
#             continue
#
#     form = ShippingAddressForm(
#         request.POST or None
#     )
#
#     if request.method == 'POST' and form.is_valid():
#
#         shipping = form.save(
#             commit=False
#         )
#
#         shipping.user = request.user
#         shipping.save()
#
#         order = Order.objects.create(
#             user=request.user,
#             shipping_address=shipping,
#             complete=False,
#             status='Pending',
#             total_amount=total,
#             payment_method='Cash on Delivery'
#         )
#
#         for product in products:
#
#             OrderItem.objects.create(
#                 order=order,
#                 product=product,
#                 quantity=product.qty,
#                 price=product.discounted_price
#             )
#
#             # STOCK REDUCE
#             product.stock -= product.qty
#
#             # AUTO DISABLE IF OUT OF STOCK
#             if product.stock <= 0:
#                 product.stock = 0
#                 product.available = False
#
#             product.save()
#
#         # CLEAR CART
#         request.session['cart'] = {}
#         request.session.modified = True
#
#         return redirect(
#             'order_success'
#         )
#
#     return render(
#         request,
#         'orders/checkout.html',
#         {
#             'products': products,
#             'total': total,
#             'form': form,
#         }
#     )
@login_required(login_url='/login/')
def checkout_view(request):

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('product_list')

    products = []
    total = 0

    for key, item in cart.items():

        try:
            # =========================
            # OLD CART SUPPORT
            # =========================
            if isinstance(item, int):
                product_id = key
                qty = item
                size = 'M'

            else:
                product_id = key.split('_')[0]
                qty = item.get('qty', 1)
                size = item.get('size', 'M')

            product = get_object_or_404(
                Product,
                id=product_id
            )

            # =========================
            # STOCK CHECK
            # =========================
            if qty > product.stock or product.stock <= 0:
                return redirect('cart')

            # =========================
            # DYNAMIC PRODUCT DATA
            # =========================
            product.qty = qty
            product.size = size
            product.total_price = float(
                product.discounted_price
            ) * qty

            total += product.total_price
            products.append(product)

        except Product.DoesNotExist:
            continue

    # =========================
    # SHIPPING FORM
    # =========================
    form = ShippingAddressForm(
        request.POST or None
    )

    # =========================
    # ORDER PLACE
    # =========================
    if request.method == 'POST' and form.is_valid():

        shipping = form.save(
            commit=False
        )

        shipping.user = request.user
        shipping.save()

        # =========================
        # CREATE ORDER
        # =========================
        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping,
            complete=False,
            status='Pending',
            total_amount=total,
            payment_method='Cash on Delivery'
        )

        # =========================
        # ORDER ITEMS + STOCK UPDATE
        # =========================
        for product in products:

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=product.qty,
                price=product.discounted_price
            )

            # STOCK REDUCE
            product.stock -= product.qty

            # AUTO DISABLE IF OUT OF STOCK
            if product.stock <= 0:
                product.stock = 0
                product.available = False

            product.save()

        # =========================
        # SEND CUSTOMER SMS ALERT
        # =========================
        send_order_sms(
            shipping.phone,
            order.id,
            order.total_amount
        )

        # =========================
        # CLEAR CART
        # =========================
        request.session['cart'] = {}
        request.session.modified = True

        # =========================
        # SUCCESS PAGE
        # =========================
        return redirect(
            'order_success'
        )

    # =========================
    # PAGE RENDER
    # =========================
    return render(
        request,
        'orders/checkout.html',
        {
            'products': products,
            'total': total,
            'form': form,
        }
    )
# =========================
# ORDER SUCCESS
# =========================
@login_required(login_url='/login/')
def order_success_view(request):
    return render(request, 'orders/order_success.html')


# =========================
# MY ORDERS
# =========================
@login_required(login_url='/login/')
def my_orders_view(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-ordered_date')

    return render(request, 'orders/my_orders.html', {
        'orders': orders,
    })

@login_required(login_url='/login/')
def track_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/track_order.html',
        {'order': order}
    )

# @staff_member_required(login_url='/login/')
# def admin_dashboard(request):
#
#     orders = Order.objects.all().order_by('-ordered_date')
#
#     total_orders = orders.count()
#     pending_orders = orders.filter(status='Pending').count()
#     processing_orders = orders.filter(status='Processing').count()
#     shipped_orders = orders.filter(status='Shipped').count()
#     delivered_orders = orders.filter(status='Delivered').count()
#     cancelled_orders = orders.filter(status='Cancelled').count()
#
#     total_revenue = sum(
#         order.total_amount for order in orders.filter(status='Delivered')
#     )
#
#     context = {
#         'orders': orders,
#         'total_orders': total_orders,
#         'pending_orders': pending_orders,
#         'processing_orders': processing_orders,
#         'shipped_orders': shipped_orders,
#         'delivered_orders': delivered_orders,
#         'cancelled_orders': cancelled_orders,
#         'total_revenue': total_revenue,
#     }
#
#     return render(request, 'admin_dashboard.html', context)
@staff_member_required(login_url='/login/')
def admin_dashboard(request):

    # ALL ORDERS
    orders = Order.objects.all().order_by('-ordered_date')

    # ALL PRODUCTS
    products = Product.objects.all().order_by('-created')

    # ORDER COUNTS
    total_orders = orders.count()
    pending_orders = orders.filter(status='Pending').count()
    processing_orders = orders.filter(status='Processing').count()
    shipped_orders = orders.filter(status='Shipped').count()
    delivered_orders = orders.filter(status='Delivered').count()
    cancelled_orders = orders.filter(status='Cancelled').count()

    # TOTAL REVENUE ONLY DELIVERED
    total_revenue = sum(
        order.total_amount for order in orders.filter(status='Delivered')
    )

    context = {
        'orders': orders,
        'products': products,   # IMPORTANT PRODUCT LIST
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'total_revenue': total_revenue,
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )

# @staff_member_required(login_url='/login/')
# def update_order_status(request, order_id, status):
#
#     order = get_object_or_404(Order, id=order_id)
#
#     valid_statuses = [
#         'Pending',
#         'Processing',
#         'Shipped',
#         'Delivered',
#         'Cancelled'
#     ]
#
#     if status in valid_statuses:
#         order.status = status
#         order.save()
#
#     return redirect('admin_dashboard')

@staff_member_required(login_url='/login/')
def update_order_status(request, order_id, status):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    valid_statuses = [
        'Pending',
        'Processing',
        'Shipped',
        'Delivered',
        'Cancelled'
    ]

    if status in valid_statuses:
        order.status = status

        # COMPLETE TRUE WHEN DELIVERED
        if status == 'Delivered':
            order.complete = True
        else:
            order.complete = False

        order.save()

    return redirect('admin_dashboard')


def apply_coupon(request):

    if request.method == 'POST':

        code = request.POST.get('coupon_code')

        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )

            request.session['coupon_id'] = coupon.id

        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return redirect('cart')


@login_required(login_url='/login/')
def payment_view(request):

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    products = []
    total = 0

    for key, item in cart.items():

        product_id = key.split('_')[0]
        product = get_object_or_404(Product, id=product_id)

        if isinstance(item, int):
            qty = item
        else:
            qty = item.get('qty', 1)

        product.qty = qty
        product.total_price = float(product.discounted_price) * qty

        total += product.total_price
        products.append(product)

    # Coupon support
    coupon_discount = 0
    coupon_id = request.session.get('coupon_id')

    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id, active=True)
            coupon_discount = (
                total * coupon.discount_percentage
            ) / 100
        except:
            pass

    final_total = total - coupon_discount

    # Razorpay client
    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        "amount": int(final_total * 100),  # paise
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        'payment': payment,
        'products': products,
        'total': final_total,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    }

    return render(
        request,
        'orders/payment.html',
        context
    )

@login_required(login_url='/login/')
def payment_success(request):

    if request.method == "POST":

        shipping = ShippingAddress.objects.filter(
            user=request.user
        ).last()

        total = request.POST.get('total')

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping,
            complete=True,
            status='Processing',
            total_amount=total,
            payment_method='Razorpay'
        )

        cart = request.session.get('cart', {})

        for key, item in cart.items():

            product_id = key.split('_')[0]
            product = Product.objects.get(id=product_id)

            if isinstance(item, int):
                qty = item
            else:
                qty = item.get('qty', 1)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                price=product.discounted_price
            )

            product.stock -= qty

            if product.stock <= 0:
                product.stock = 0
                product.available = False

            product.save()

        request.session['cart'] = {}
        request.session['coupon_id'] = None
        request.session.modified = True

        return redirect('order_success')

    return redirect('cart')