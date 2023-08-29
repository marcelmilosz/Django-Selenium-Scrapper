from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Product

from .Selenium import main as myScrapper

# Create your views here.

def index(request):
    # Retrieve all Product instances
    products = Product.objects.all()

    # Pass the products to the template context
    context = {'products': products}

    # Render the template
    return render(request, 'AllegroScrapper/index.html', context)


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('index-page')  # Redirect to the product list page

def run_scrapper(request, ean):

    try:
        Scrapper = myScrapper.SingleProductScrapper(ean)
        scrapper_data = Scrapper.start()

        defaults = {
            field: scrapper_data.get(field)
            for field in [
                "offer_link",
                "how_many_offers",
                "best_title",
                "max_howManyBought",
                "best_price",
                "lowest_price",
                "highest_price",
                "avg_price",
                "best_offer_link",
                "best_description",
                "parameters",
                "photos_links",
                "first_photo_link",
                "product_category",
                "product_category_id",
                "howManyBought",
                "best_offer_owner",
                "best_offer_delivery_costs",
                "product_rating",
                "product_opinions",
            ]
        }

        product_instance, created = Product.objects.update_or_create(
            product_or_ean=ean, defaults=defaults
        )

        print("Product added or updated correctly")
        return redirect("/?succes=1")
    
    except Exception as e:

        print("Something went wrong!")
        print(e)

        return redirect("/?succes=0")
