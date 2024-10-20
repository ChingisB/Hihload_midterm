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
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from products.views import (
    ProductListCreateView, ProductDetailView,
    CategoryListCreateView, CategoryDetailView,
    ProductInventoryView
)
from orders.views import(
    CustomerCreateView, CustomerDetailView, 
    OrderInfoView, ShippingAddressCreateView, ShippingAddressDetailView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Product URLs
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/inventory/', ProductInventoryView.as_view(), name='product-inventory'),

    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('customer/info/create/', CustomerCreateView.as_view(), name="create_customer_info"),
    path('customer/info/', CustomerDetailView.as_view(), name="retrieve_customer_info"),
    path('orders/', OrderInfoView.as_view(), name="orders"),
    path('orders/<int:order_id>', OrderInfoView.as_view(), name="concrete_order"),
    path('address/create', ShippingAddressCreateView.as_view(), name="create_shipping_address"),
    path('adress/', ShippingAddressDetailView.as_view(), name="retrive_shipping_address"),
    path('adress/create', ShippingAddressDetailView.as_view(), name="retrive_shipping_address"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
