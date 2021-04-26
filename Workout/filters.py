import django_filters
from django_filters import CharFilter

from .models import *

class FriendFilter(django_filters.FilterSet):
    username = CharFilter(field_name = 'username' , lookup_expr = 'icontains')
    class Meta:
        model = Customer
        fields = ['username']

class TextFilter(django_filters.FilterSet):
    text = CharFilter(field_name = 'text' , lookup_expr = 'icontains')
    class Meta:
        model = Dialogues
        fields = ['text']