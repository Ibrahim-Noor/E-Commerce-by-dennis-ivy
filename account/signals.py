from django.db.models.signals import post_save
from .models import CustomUserManager, Account
from store.models import Customer
from django.dispatch import receiver


@receiver(post_save, sender=Account)
def customer_profile(sender, instance, created, **kwargs):
    print('sender:  ', sender)
    print('instance:  ', instance)
    print('created:  ', created)
    print('kwargs', kwargs)
    if created:
        customer, create = Customer.objects.get_or_create(email=instance.email)
        customer.user = instance
        if create:
            customer.name = instance.username
        customer.save()
