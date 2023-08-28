from django.db import models
from datetime import datetime

# Create your models here.
class Product(models.Model):
    product_or_ean = models.CharField(max_length=200)  # Allow an empty value in forms
    how_many_offers = models.IntegerField(blank=True, null=True)  # Allow an empty value in forms and NULL in the database
    offer_link = models.TextField(blank=True, null=True)  # Allow an empty value in forms and NULL in the database
    best_title = models.TextField(blank=True)
    max_howManyBought = models.IntegerField(blank=True, null=True)
    best_price = models.FloatField(blank=True, null=True)
    lowest_price = models.FloatField(blank=True, null=True)
    highest_price = models.FloatField(blank=True, null=True)
    avg_price = models.FloatField(blank=True, null=True)
    best_offer_link = models.TextField(blank=True, null=True)
    best_description = models.TextField(blank=True, null=True)
    parameters = models.TextField(blank=True, null=True)
    photos_links = models.TextField(blank=True, null=True)
    first_photo_link = models.TextField(blank=True, null=True)
    product_category = models.TextField(blank=True, null=True)
    date_added = models.DateField(default=datetime.now)

    def __str__(self):
        return str(self.id) + ". " + self.product_or_ean  + " " + self.best_title