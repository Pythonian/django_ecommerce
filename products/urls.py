from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('c/<slug:category_slug>/', views.product_list, name='category'),
    path('vote/', views.vote_review, name="vote_review"),
    path('search/', views.product_search, name='search'),
    path('new/', views.product_create, name='create'),
    path('<int:id>/', views.product_update, name='update'),
    path('<slug:slug>/', views.product_detail, name='detail'),
]
