from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
import json
from .utils import cookieCart, cartData, guestOrder
from .forms import *
from decimal import Decimal

# Create your views here.


def store_view(request):
    context = {}
    data = cartData(request)
    cart_items = data['cart_items']
    products = Product.objects.all()
    context['products'] = products
    context['cart_items'] = cart_items
    return render(request, 'store/store.html', context)


def cart_view(request):
    context = {}
    data = cartData(request)
    cart_items = data['cart_items']
    items = data['items']
    order = data['order']
    context['items'] = items
    context['order'] = order
    context['cart_items'] = cart_items
    return render(request, 'store/cart.html', context)


def checkout_view(request):
    context = {}
    data = cartData(request)
    cart_items = data['cart_items']
    items = data['items']
    order = data['order']
    user_info_form = UserInfoForm()
    shipping_address_form = ShippingAddressForm()
    if request.user.is_authenticated:
        customer = request.user.customer
        user_info_form = UserInfoForm(instance=customer)
        shipping_address = request.user.customer.shipping_address
        shipping_address_form = ShippingAddressForm(instance=shipping_address)
    context['user_info_form'] = user_info_form
    context['shipping_address_form'] = shipping_address_form
    context['items'] = items
    context['order'] = order
    context['cart_items'] = cart_items
    # context['order'] = order
    return render(request, 'store/checkout.html', context)


def update_item_view(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']
    print('action: ', action)
    print('product_id: ', product_id)
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        product=product, order=order)
    if action == 'add':
        order_item.quantity = order_item.quantity + 1
    elif action == 'remove':
        order_item.quantity = order_item.quantity - 1
    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse(order.get_cart_items, safe=False)


def process_order_view(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = Decimal(data['form']['total'])
    order.transaction_id = transaction_id
    if round(total, 2) == round(order.get_cart_total, 2):
        order.complete = True
        order.save()
        placed_order = PlacedOrders(
            customer=customer,
            order=order
        )
        if order.shipping == True:
            shipping_address = ShippingAddress(address=data['shipping']['address'],
                                               city=data['shipping']['city'],
                                               state=data['shipping']['state'],
                                               zipcode=data['shipping']['zipcode'])
            if customer.shipping_address != None:
                if customer.shipping_address != shipping_address:
                    customer_shipping_address = customer.shipping_address
                    customer_shipping_address.address = shipping_address.address
                    customer_shipping_address.city = shipping_address.city
                    customer_shipping_address.state = shipping_address.state
                    customer_shipping_address.zipcode = shipping_address.zipcode
                    customer_shipping_address.save()
            else:
                shipping_address.save()
                customer.shipping_address = shipping_address
                customer.save()

            placed_order.shipping_address = customer.shipping_address
        placed_order.save()
        return JsonResponse('payment complete', safe=False)
    else:
        return JsonResponse('Order Could not be placed', safe=False)
