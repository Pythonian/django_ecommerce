from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('logout/',
         auth_views.LogoutView.as_view(), name='logout'),
    path('login/',
         auth_views.LoginView.as_view(
             redirect_authenticated_user=True), name='login'),

    # Registration
    path('vendor/signup/', views.vendor_signup, name='vendor_signup'),
    path('customer/signup/', views.customer_signup, name='customer_signup'),

    # password change
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),

    # Customer account
    path('customer/', views.customer_account, name='customer'),
    path('customer/orders/', views.customer_orders, name='orders'),
    path('customer/addresses/', views.customer_addresses, name='addresses'),
    path('customer/wishlists/', views.customer_wishlist, name='wishlist'),

    # Vendor account
    path('vendors/', views.vendors, name='vendors'),
    path('vendor/', views.vendor_account, name='vendor'),
    path('vendor/orders/', views.vendor_orders, name='vendor_orders'),
    path('vendor/products/', views.vendor_products, name='vendor_products'),
    path('vendor/<str:username>/',
         views.vendor_profile, name='vendor_profile'),

    path('deactivate/', views.deactivate, name='deactivate'),
]
