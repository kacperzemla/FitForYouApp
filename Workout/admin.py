from django.contrib import admin

# Register your models here.

from .models import Customer,Equipment,Exercises,Training, Meal

admin.site.register(Customer)
admin.site.register(Equipment)
admin.site.register(Exercises)
admin.site.register(Training)
admin.site.register(Meal)
