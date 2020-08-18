from django.db import models
from django.conf import settings


class ShippingAddress(models.Model):
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="user",
                                on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    shipping_address = models.OneToOneField(
        ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, blank=False, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        url = None
        try:
            url = self.image.url
        except:
            url = '/images/placeholder.jpg'
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        orderitems = self.orderitem_set.all()
        for orderitem in orderitems:
            if orderitem.product.digital == False:
                return True
        return False


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        return (self.quantity * self.product.price)


class PlacedOrders(models.Model):
    STATUS = (('pending', 'pending'),
              ('On the way', 'on the way'),
              ('Delivered', 'delivere'),
              ('Cancelled', 'cancelled'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(
        max_length=200, choices=STATUS, default=STATUS[0][0])
    date_added = models.DateTimeField(auto_now_add=True)
