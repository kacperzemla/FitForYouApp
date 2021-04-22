from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _
from .models import Training, Exercises


class TrainingForm(ModelForm):
   class Meta:
      model = Training
      fields = ['exercise','weigth','sesion','reps']

class ExerciseForm(ModelForm):
   class Meta:
      model = Exercises
      fields =['name','category']

class CreateUserForm(UserCreationForm):

   class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2' ]



