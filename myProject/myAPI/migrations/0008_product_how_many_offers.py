# Generated by Django 4.2.4 on 2023-08-25 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myAPI', '0007_alter_product_max_howmanybought'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='how_many_offers',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]