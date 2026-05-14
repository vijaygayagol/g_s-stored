# =========================
# accounts/views.py
# =========================

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from orders.models import Order
from django.contrib import messages

# def register_view(request):
#
#     form = RegisterForm(request.POST or None)
#
#     if form.is_valid():
#         user = form.save()
#
#         login(request, user)
#
#         return redirect('home')
#
#     return render(request, 'accounts/register.html', {
#         'form': form
#     })

def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Registration successful!"
            )

            return redirect('home')

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


def logout_view(request):
    logout(request)

    return redirect('login')


@login_required(login_url='/login/')
def dashboard_view(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-ordered_date')

    total_orders = orders.count()

    return render(request, 'accounts/dashboard.html', {
        'orders': orders,
        'total_orders': total_orders,
    })