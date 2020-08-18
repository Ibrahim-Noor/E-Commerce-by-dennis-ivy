from django.urls import path
from .views import *
urlpatterns = [
    path('', store_view, name="store"),
    path('cart/', cart_view, name="cart"),
    path('checkout/', checkout_view, name="checkout"),
    path('update-item/', update_item_view, name="update-item"),
    path('process-order/', process_order_view, name='process-order'),
]
