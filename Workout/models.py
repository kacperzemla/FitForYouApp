from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    # on_delete= models.CASCADE jezeli usuniemy uzytkownika tego glownego to to powiazanie tez zostanie usuniete
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)
    number = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    weight = models.IntegerField(null=True)
    height = models.IntegerField(null=True)


class Equipment(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Exercises(models.Model):

    CATEGORY = (
        ('chest', 'chest'),
        ('leg', 'leg'),
        ('abs', 'abs'),
        ('arms', 'arms')
    )

    name = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50, null=True, choices=CATEGORY)

    def __str__(self):
        return self.name


class Training(models.Model):

    date = models.DateTimeField(auto_now_add=True, null=True)
    exercise = models.ForeignKey(
        Exercises, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    weigth = models.IntegerField(null=True)
    sesion = models.IntegerField(null=True)
    reps = models.IntegerField(null=True)

    def __str__(self):
        return self.exercise.name


class Meal(models.Model):
    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, null=True)
    carbs = models.IntegerField(null=True)
    fats = models.IntegerField(null=True)
    proteins = models.IntegerField(null=True)
    kcal = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date = models.DateTimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.name
