from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _
from .models import *

class TrainingForm(ModelForm):
   class Meta:
      model = Training
      fields = ['exercise','weigth','sesion','reps']
      
   def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'weight_input'

class RelationsForm(ModelForm):
   class meta:
      model = Relations
      fields = [all]

class ExerciseForm(ModelForm):
   class Meta:
      model = Exercises
      fields =['name','category']

class CreateUserForm(UserCreationForm):

   class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2' ]

class CustomerForm(ModelForm):

   class Meta:
      model = Customer
      fields = '__all__'
      exclude = ['user'] #wyrzucamy z pol usera bo przeciez tego sie nie da zmienic

   def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'weight_input'

