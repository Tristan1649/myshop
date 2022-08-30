import django_filters.rest_framework

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


@staff_member_required
def admin_order_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = {
        'category': category
    }
    return render(request, 'admin/shop/category/detail.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'shop/product/detail.html', context)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def delete(self, request, *args, **kwargs):
        print(request.method)
        return self.destroy(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        print("делаем то что нам надо")
        # do something
        return self.partial_update(request, *args, **kwargs)
    

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['category']
    pagination_class = StandardResultsSetPagination

    


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
