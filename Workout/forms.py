from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _
from .models import *


class TrainingForm(ModelForm):
   class Meta:
      model = Training
      fields = ['exercise','weigth']


class CreateUserForm(UserCreationForm):

   class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2' ]

class CustomerForm(ModelForm):

   class Meta:
      model = Customer
      fields = '__all__'
      exclude = ['user'] #wyrzucamy z pol usera bo przeciez tego sie nie da zmienic


