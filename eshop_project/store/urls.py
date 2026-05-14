

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),

    path(
        'products/',
        views.product_list_view,
        name='product_list'
    ),

    path(
        'product/<slug:slug>/',
        views.product_detail_view,
        name='product_detail'
    ),

    path(
        'category/<slug:category_slug>/',
        views.category_view,
        name='category_view'
    ),

    path(
        'search/',
        views.search_view,
        name='search'
    ),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('about/', views.about_view, name='about'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path(
        'add-review/<int:product_id>/',
        views.add_review,
        name='add_review'
    ),
    path(
        'manage-reviews/',
        views.manage_reviews,
        name='manage_reviews'
    ),
    path(
        'product/<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
