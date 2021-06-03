# Generated by Django 3.2 on 2021-05-08 18:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Workout', '0013_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='height',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(400)]),
        ),
    ]
