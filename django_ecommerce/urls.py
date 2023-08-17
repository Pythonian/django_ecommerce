"""django_ecommerce URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from orders.admin import dispatch_site
from .views import home, update_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dispatchadmin/', dispatch_site.urls),
    path('cart/', include('carts.urls', namespace='carts')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('products/', include('products.urls', namespace='products')),
    path('update-cart/', update_cart, name='update_cart'),

        # password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('paystack/', include(('paystack.frameworks.django.urls', 'paystack'), namespace='paystack')),

    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.index_title = 'MirajayKart'
admin.site.site_header = 'MirajayKart Admin'
admin.site.site_title = 'Control Panel'
