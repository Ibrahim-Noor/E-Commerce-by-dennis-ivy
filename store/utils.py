import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cart_items = order['get_cart_items']
    for cart_item in cart:
        cart_items += cart[cart_item]['quantity']
        try:
            product = Product.objects.get(id=cart_item)
        except:
            continue
        total = product.price * cart[cart_item]['quantity']
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[cart_item]['quantity']

        item = {'product': {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'imageURL': product.imageURL
        },
            'quantity': cart[cart_item]['quantity'],
            'get_total': total,
        }
        items.append(item)
        if product.digital == False:
            order['shipping'] = True
    return {'cart_items': cart_items, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cart_items = cookieData['cart_items']
        items = cookieData['items']
        order = cookieData['order']
    return {'cart_items': cart_items, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(email=email)
    if created:
        customer.name = name
        customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order
