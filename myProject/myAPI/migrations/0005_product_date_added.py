# Generated by Django 4.2.4 on 2023-08-25 11:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAPI', '0004_product_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_added',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]