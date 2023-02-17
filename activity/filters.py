from dataclasses import fields
from pyexpat import model
import django_filters 
from  .models import *

class homefilter(django_filters.FilterSet):
    class Meta:
        model = home
        fields = ['Hometype','Price','Location']


class listingfilter(django_filters.FilterSet):
    class Meta:
        model = homelisting
        fields = ['category',
            'hometype',
            'bedrooms',
            'location',
            'price'
            ]
