from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Product
import json

from .Selenium import main as myScrapper

# Create your views here.

def index(request):
    # Retrieve all Product instances
    products = Product.objects.all()

    # Pass the products to the template context
    context = {'products': products}

    # Render the template
    return render(request, 'myAPI/index.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('index-page')  # Redirect to the product list page

def run_scrapper(request, ean):

    try: 

        Scrapper = myScrapper.SingleProductScrapper(ean)
        scrapper_data = Scrapper.start()

        product_instance, created = Product.objects.get_or_create(
            product_or_ean=ean,
            defaults={
                "offer_link": scrapper_data.get("offer_link"),
                "how_many_offers": scrapper_data.get("how_many_offers"),
                "best_title": scrapper_data.get("best_title"),
                "max_howManyBought": scrapper_data.get("max_howManyBought"),
                "best_price": scrapper_data.get("best_price"),
                "lowest_price": scrapper_data.get("lowest_price"),
                "highest_price": scrapper_data.get("highest_price"),
                "avg_price": scrapper_data.get("avg_price"),
                "best_offer_link": scrapper_data.get("best_offer_link"),
                "best_description": scrapper_data.get("best_description"),
                "parameters": scrapper_data.get("parameters"),
                "photos_links": scrapper_data.get("photos_links"),
                "first_photo_link": scrapper_data.get("first_photo_link"),
                "product_category": scrapper_data.get("product_category")
            }
        )

        # If not created, update the instance's fields
        if not created:
            product_instance.offer_link = scrapper_data.get("offer_link")
            product_instance.how_many_offers = scrapper_data.get("how_many_offers")
            product_instance.best_title = scrapper_data.get("best_title")
            product_instance.max_howManyBought = scrapper_data.get("max_howManyBought")
            product_instance.best_price = scrapper_data.get("best_price")
            product_instance.lowest_price = scrapper_data.get("lowest_price")
            product_instance.highest_price = scrapper_data.get("highest_price")
            product_instance.avg_price = scrapper_data.get("avg_price")
            product_instance.best_offer_link = scrapper_data.get("best_offer_link")
            product_instance.best_description = scrapper_data.get("best_description")
            product_instance.parameters = scrapper_data.get("parameters")
            product_instance.photos_links = scrapper_data.get("photos_links")
            product_instance.first_photo_link = scrapper_data.get("first_photo_link")
            product_instance.product_category = scrapper_data.get("product_category")
            product_instance.save()

        return redirect("/?succes=1")
    
    except Exception as e:

        return redirect("/?succes=0")
