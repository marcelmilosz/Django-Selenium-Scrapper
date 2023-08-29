# Generated by Django 4.2.4 on 2023-08-29 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAPI', '0011_alter_product_best_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='best_offer_delivery_costs',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='best_offer_owner',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_opinions',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='product_rating',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
