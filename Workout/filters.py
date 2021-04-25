import django_filters

from .models import *

class FriendFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['username']