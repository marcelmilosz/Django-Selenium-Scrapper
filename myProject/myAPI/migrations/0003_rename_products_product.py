# Generated by Django 4.2.4 on 2023-08-25 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myAPI', '0002_remove_products_best_offer_price_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]