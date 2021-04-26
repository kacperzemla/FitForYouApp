import django_filters

from .models import *

class FriendFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['username']

class TextFilter(django_filters.FilterSet):
    class Meta:
        model = Dialogues
        fields = ['text']