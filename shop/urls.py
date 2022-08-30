from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('category/', views.CategoryList.as_view()),
    path('category/<int:pk>/', views.CategoryDetail.as_view()),
    path('product/', views.ProductList.as_view()),
    path('product/<int:pk>/', views.ProductDetail.as_view()),

    path('', views.product_list, name='product-list'),        
    path('<slug:category_slug>/', views.product_list, name='product-list-by-category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product-detail'),
    # path для админки, как в ордер
]