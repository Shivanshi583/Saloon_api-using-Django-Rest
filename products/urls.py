from django.urls import path

from products.views import ProductView, ProductIdView
     



urlpatterns = [
    path('product/', ProductView.as_view(), name="product_create_read"),
    path('product/<uuid:product_id>/', ProductIdView.as_view(), name="product_update_delete"),
    
]       