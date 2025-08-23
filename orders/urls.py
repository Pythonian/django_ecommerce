from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='create'),
    path("admin/order/<int:order_id>/", views.admin_order_detail, name="admin_order_detail"),
    path("admin/order/<int:order_id>/pdf/", views.admin_order_pdf, name="admin_order_pdf"),
    path('track-order/<int:id>/', views.track_order, name='track_order'),
    path('status/shipped/<int:id>/',
         views.order_status_shipped, name='order_status_shipped'),
    path('status/processing/<int:id>/',
         views.order_status_processing, name='order_status_processing'),
    path('status/completed/<int:id>/',
         views.order_status_completed, name='order_status_completed'),
]
