import email
import imp
from unicodedata import name
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group

from .models import customer

def customer_profile(sender,instance,created,**kwargs):
    if created :
        group, created = Group.objects.get_or_create(name='customer')
        instance.groups.add(group)

        customer.objects.create(
            user = instance,
            email=instance.email
             
        )
        print('profile created')

post_save.connect(customer_profile,sender=User)
