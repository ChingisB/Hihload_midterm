"""
URL configuration for online_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken.views import obtain_auth_token
from products.views import (
    ProductListCreateView, ProductDetailView,
    CategoryListCreateView, CategoryDetailView,
    ProductInventoryView
)
from orders.views import(
    CustomerCreateView, CustomerDetailView, 
    OrderInfoView, ShippingAddressCreateView, ShippingAddressDetailView
)

schema_view = get_swagger_view(title='China Shop')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Product URLs
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/inventory/', ProductInventoryView.as_view(), name='product-inventory'),

    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('customer/info/create/', CustomerCreateView.as_view(), name="create_customer_info"),
    path('customer/info/', CustomerDetailView.as_view(), name="retrieve_customer_info"),
    path('orders/', OrderInfoView.as_view(), name="orders"),
    path('address/create', ShippingAddressCreateView.as_view(), name="create_shipping_address"),
    path('adress/', ShippingAddressDetailView.as_view(), name="retrive_shipping_address"),
    path('/', schema_view, name="swagger"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
