from django.contrib import admin

# Register your models here.

from .models import Customer,Exercises,Training, Meal,Relations,Dialogues

admin.site.register(Customer)
admin.site.register(Exercises)
admin.site.register(Training)
admin.site.register(Meal)
admin.site.register(Relations)
admin.site.register(Dialogues)

