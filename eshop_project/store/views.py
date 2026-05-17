# COMPLETE FUNCTIONAL VIEWS FOR ALL URLS
# Yeh code direct respective files me paste karo


# =========================
# store/views.py
# =========================

# from django.shortcuts import render, get_object_or_404
# from django.db.models import Q
# from .models import Product, Category
# from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Category, Product
# from .forms import CategoryForm, ProductForm
# from .models import Product, ProductReview ,Wishlist
# from .forms import ProductReviewForm
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# # def home_view(request):
# #     products = Product.objects.filter(available=True)[:8]
# #     categories = Category.objects.all()
# #
# #     return render(
# #         request,
# #         'home.html',
# #         {
# #             'products': products
# #         }
# #     )
# def home_view(request):
#     products = Product.objects.filter(available=True)[:8]
#     categories = Category.objects.all()
#
#     return render(request, 'home.html', {
#         'products': products,
#         'categories': categories,
#     })
#
#
# def product_list_view(request):
#     products = Product.objects.filter(available=True)
#     categories = Category.objects.all()
#
#     return render(request, 'store/product_list.html', {
#         'products': products,
#         'categories': categories,
#     })
#
#
# def product_detail_view(request, slug):
#     product = get_object_or_404(
#         Product,
#         slug=slug,
#         available=True
#     )
#
#     categories = Category.objects.all()
#
#     return render(request, 'store/product_detail.html', {
#         'product': product,
#         'categories': categories,
#     })
#
#
# def category_view(request, category_slug):
#     category = get_object_or_404(
#         Category,
#         slug=category_slug
#     )
#
#     categories = Category.objects.all()
#
#     products = Product.objects.filter(
#         category=category,
#         available=True
#     )
#
#     return render(request, 'store/product_list.html', {
#         'products': products,
#         'categories': categories,
#         'selected_category': category,
#     })
#
# def category_products(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#
#     products = Product.objects.filter(
#         category=category,
#         available=True
#     )
#
#     return render(request, 'store/category_products.html', {
#         'category': category,
#         'products': products
#     })
#
# def search_view(request):
#     query = request.GET.get('q', '')
#
#     categories = Category.objects.all()
#
#     products = Product.objects.filter(
#         Q(name__icontains=query) |
#         Q(description__icontains=query),
#         available=True
#     )
#
#     return render(request, 'store/search_results.html', {
#         'products': products,
#         'query': query,
#         'categories': categories,
#     })
#
# def about_view(request):
#     return render(request, 'store/about.html')
#
#
# # CATEGORY ADD
# @staff_member_required
# def add_category(request):
#
#     form = CategoryForm(request.POST or None, request.FILES or None)
#
#     if form.is_valid():
#         form.save()
#         return redirect('admin_dashboard')
#
#     return render(request, 'admin/add_category.html', {
#         'form': form
#     })
#
#
# # PRODUCT ADD
# @staff_member_required
# def add_product(request):
#
#     form = ProductForm(request.POST or None, request.FILES or None)
#
#     if form.is_valid():
#         form.save()
#         return redirect('admin_dashboard')
#
#     return render(request, 'admin/add_product.html', {
#         'form': form
#     })
#
#
# # PRODUCT EDIT
# @staff_member_required
# def edit_product(request, product_id):
#
#     product = get_object_or_404(Product, id=product_id)
#
#     form = ProductForm(
#         request.POST or None,
#         request.FILES or None,
#         instance=product
#     )
#
#     if form.is_valid():
#         form.save()
#         return redirect('admin_dashboard')
#
#     return render(request, 'admin/edit_product.html', {
#         'form': form,
#         'product': product
#     })
#
#
# # PRODUCT DELETE
# @staff_member_required
# def delete_product(request, product_id):
#
#     product = get_object_or_404(Product, id=product_id)
#     product.delete()
#
#     return redirect('admin_dashboard')
#
# # def product_detail(request, slug):
# #     product = get_object_or_404(Product, slug=slug)
# #     reviews = product.reviews.all()
# #
# #     form = ProductReviewForm()
# #
# #     context = {
# #         'product': product,
# #         'reviews': reviews,
# #         'form': form,
# #     }
# #
# #     return render(request, 'product_detail.html', context)
# # =========================
# # PRODUCT DETAIL PAGE
# # =========================
# def product_detail(request, slug):
#
#     product = get_object_or_404(
#         Product,
#         slug=slug
#     )
#
#     # ALL REVIEWS FOR THIS PRODUCT
#     reviews = ProductReview.objects.filter(
#         product=product
#     ).order_by('-created_at')
#
#     # AVERAGE RATING
#     total_reviews = reviews.count()
#
#     if total_reviews > 0:
#         average_rating = round(
#             sum(review.rating for review in reviews) / total_reviews,
#             1
#         )
#     else:
#         average_rating = 0
#
#     context = {
#         'product': product,
#         'reviews': reviews,
#         'total_reviews': total_reviews,
#         'average_rating': average_rating,
#     }
#
#     return render(
#         request,
#         'store/product_detail.html',
#         context
#     )
#
#
# # =========================
# # ADD REVIEW
# # =========================
# @login_required(login_url='/login/')
# def add_review(request, product_id):
#
#     product = get_object_or_404(
#         Product,
#         id=product_id
#     )
#
#     if request.method == "POST":
#
#         rating = request.POST.get('rating')
#         comment = request.POST.get('comment')
#
#         # CHECK IF USER ALREADY REVIEWED
#         existing_review = ProductReview.objects.filter(
#             product=product,
#             user=request.user
#         ).first()
#
#         if existing_review:
#             existing_review.rating = rating
#             existing_review.comment = comment
#             existing_review.save()
#
#             messages.success(
#                 request,
#                 "Your review has been updated successfully."
#             )
#
#         else:
#             ProductReview.objects.create(
#                 product=product,
#                 user=request.user,
#                 rating=rating,
#                 comment=comment
#             )
#
#             messages.success(
#                 request,
#                 "Your review has been submitted successfully."
#             )
#
#     return redirect(
#         'product_detail',
#         slug=product.slug
#     )
#
#
# # =========================
# # ADMIN REVIEW MANAGEMENT
# # =========================
# @staff_member_required(login_url='/login/')
# def manage_reviews(request):
#
#     reviews = ProductReview.objects.all().order_by(
#         '-created_at'
#     )
#
#     total_reviews = reviews.count()
#
#     context = {
#         'reviews': reviews,
#         'total_reviews': total_reviews,
#     }
#
#     return render(
#         request,
#         'manage_reviews.html',
#         context
#     )
#
#
# # =========================
# # DELETE REVIEW (ADMIN)
# # =========================
# @staff_member_required(login_url='/login/')
# def delete_review(request, review_id):
#
#     review = get_object_or_404(
#         ProductReview,
#         id=review_id
#     )
#
#     review.delete()
#
#     messages.success(
#         request,
#         "Review deleted successfully."
#     )
#
#     return redirect('manage_reviews')
#
#
# @login_required(login_url='/login/')
# def add_to_wishlist(request, product_id):
#
#     product = get_object_or_404(Product, id=product_id)
#
#     Wishlist.objects.get_or_create(
#         user=request.user,
#         product=product
#     )
#
#     return redirect('wishlist')
#
#
# @login_required(login_url='/login/')
# def wishlist_view(request):
#
#     wishlist_items = Wishlist.objects.filter(
#         user=request.user
#     ).select_related('product')
#
#     return render(
#         request,
#         'store/wishlist.html',
#         {
#             'wishlist_items': wishlist_items
#         }
#     )
#
#
# @login_required(login_url='/login/')
# def remove_from_wishlist(request, product_id):
#
#     Wishlist.objects.filter(
#         user=request.user,
#         product_id=product_id
#     ).delete()
#
#     return redirect('wishlist')



from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    Product,
    Category,
    ProductReview,
    Wishlist,
    ProductImage
)

from .forms import (
    CategoryForm,
    ProductForm,
    ProductReviewForm
)


# =========================
# HOME PAGE
# =========================
def home_view(request):

    products = Product.objects.filter(
        available=True
    )[:8]

    categories = Category.objects.all()

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories,
        }
    )


# =========================
# PRODUCT LIST PAGE
# =========================
def product_list_view(request):

    products = Product.objects.filter(
        available=True
    )

    categories = Category.objects.all()

    return render(
        request,
        'store/product_list.html',
        {
            'products': products,
            'categories': categories,
        }
    )


# =========================
# PRODUCT DETAIL PAGE
# =========================
def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        available=True
    )

    categories = Category.objects.all()

    # PRODUCT REVIEWS
    reviews = ProductReview.objects.filter(
        product=product
    ).order_by('-created_at')

    # PRODUCT GALLERY
    # gallery_images = ProductImage.objects.filter(
    #     product=product
    # )
    gallery_images = product.gallery_images.all()

    # AVERAGE RATING
    total_reviews = reviews.count()

    if total_reviews > 0:
        average_rating = round(
            sum(review.rating for review in reviews) / total_reviews,
            1
        )
    else:
        average_rating = 0

    # USER WISHLIST STATUS
    in_wishlist = False

    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()

    context = {
        'product': product,
        'categories': categories,
        'reviews': reviews,
        'gallery_images': gallery_images,
        'total_reviews': total_reviews,
        'average_rating': average_rating,
        'in_wishlist': in_wishlist,
    }

    return render(
        request,
        'store/product_detail.html',
        context
    )


# =========================
# PRODUCT DETAIL VIEW ALIAS
# =========================
def product_detail_view(request, slug):
    return product_detail(request, slug)


# =========================
# CATEGORY FILTER
# =========================
def category_view(request, category_slug):

    category = get_object_or_404(
        Category,
        slug=category_slug
    )

    categories = Category.objects.all()

    products = Product.objects.filter(
        category=category,
        available=True
    )

    return render(
        request,
        'store/product_list.html',
        {
            'products': products,
            'categories': categories,
            'selected_category': category,
        }
    )


# =========================
# CATEGORY PRODUCTS PAGE
# =========================
def category_products(request, slug):

    category = get_object_or_404(
        Category,
        slug=slug
    )

    products = Product.objects.filter(
        category=category,
        available=True
    )

    return render(
        request,
        'store/category_products.html',
        {
            'category': category,
            'products': products
        }
    )


# =========================
# SEARCH
# =========================
def search_view(request):

    query = request.GET.get(
        'q',
        ''
    )

    categories = Category.objects.all()

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query),
        available=True
    )

    return render(
        request,
        'store/search_results.html',
        {
            'products': products,
            'query': query,
            'categories': categories,
        }
    )


# =========================
# ABOUT PAGE
# =========================
def about_view(request):
    return render(
        request,
        'store/about.html'
    )


# =========================
# ADD CATEGORY
# =========================
@staff_member_required
def add_category(request):

    form = CategoryForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Category added successfully."
        )
        return redirect(
            'admin_dashboard'
        )

    return render(
        request,
        'admin/add_category.html',
        {
            'form': form
        }
    )


# =========================
# ADD PRODUCT
# =========================
@staff_member_required
def add_product(request):

    form = ProductForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        product = form.save()

        messages.success(
            request,
            "Product added successfully."
        )

        return redirect(
            'admin_dashboard'
        )

    return render(
        request,
        'admin/add_product.html',
        {
            'form': form
        }
    )


# =========================
# EDIT PRODUCT
# =========================
@staff_member_required
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            "Product updated successfully."
        )

        return redirect(
            'admin_dashboard'
        )

    return render(
        request,
        'admin/edit_product.html',
        {
            'form': form,
            'product': product
        }
    )


# =========================
# DELETE PRODUCT
# =========================
@staff_member_required
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    product.delete()

    messages.success(
        request,
        "Product deleted successfully."
    )

    return redirect(
        'admin_dashboard'
    )


# =========================
# ADD / UPDATE REVIEW
# =========================
@login_required(login_url='/login/')
def add_review(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == "POST":

        rating = request.POST.get(
            'rating'
        )

        comment = request.POST.get(
            'comment'
        )

        existing_review = ProductReview.objects.filter(
            product=product,
            user=request.user
        ).first()

        if existing_review:

            existing_review.rating = rating
            existing_review.comment = comment
            existing_review.save()

            messages.success(
                request,
                "Your review has been updated successfully."
            )

        else:

            ProductReview.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )

            messages.success(
                request,
                "Your review has been submitted successfully."
            )

    return redirect(
        'product_detail',
        slug=product.slug
    )


# =========================
# MANAGE REVIEWS
# =========================
@staff_member_required(login_url='/login/')
def manage_reviews(request):

    reviews = ProductReview.objects.all().order_by(
        '-created_at'
    )

    total_reviews = reviews.count()

    return render(
        request,
        'manage_reviews.html',
        {
            'reviews': reviews,
            'total_reviews': total_reviews,
        }
    )


# =========================
# DELETE REVIEW
# =========================
@staff_member_required(login_url='/login/')
def delete_review(request, review_id):

    review = get_object_or_404(
        ProductReview,
        id=review_id
    )

    review.delete()

    messages.success(
        request,
        "Review deleted successfully."
    )

    return redirect(
        'manage_reviews'
    )


# =========================
# ADD TO WISHLIST
# =========================
@login_required(login_url='/login/')
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(
        request,
        "Added to wishlist successfully."
    )

    return redirect(
        'wishlist'
    )


# =========================
# WISHLIST PAGE
# =========================
@login_required(login_url='/login/')
def wishlist_view(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related(
        'product'
    )

    return render(
        request,
        'store/wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


# =========================
# REMOVE FROM WISHLIST
# =========================
@login_required(login_url='/login/')
def remove_from_wishlist(request, product_id):

    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    messages.success(
        request,
        "Removed from wishlist."
    )

    return redirect(
        'wishlist'
    )