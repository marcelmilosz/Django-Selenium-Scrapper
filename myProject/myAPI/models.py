from django.db import models

# Create your models here.
class Product(models.Model):
    product_or_ean = models.CharField(max_length=200)  # Allow an empty value in forms
    offer_link = models.TextField(blank=True, null=True)  # Allow an empty value in forms and NULL in the database
    best_title = models.TextField(blank=True)
    max_howManyBought = models.FloatField(blank=True, null=True)
    best_price = models.FloatField(blank=True, null=True)
    lowest_price = models.FloatField(blank=True, null=True)
    highest_price = models.FloatField(blank=True, null=True)
    avg_price = models.FloatField(blank=True, null=True)
    best_offer_link = models.TextField(blank=True, null=True)
    best_description = models.TextField(blank=True)
    parameters = models.TextField(blank=True)
    photos_links = models.TextField(blank=True)

    def __str__(self):
        return str(self.id) + ". " + self.product_or_ean 