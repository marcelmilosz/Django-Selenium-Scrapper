from django.urls import path
from .views import index, run_scrapper,delete_product

urlpatterns = [
    path('', index, name="index-page"),  # Use 'name' parameter instead of the third argument
    path("run-scraper/<str:ean>", run_scrapper, name="scrapper"),
    path('delete-product/<int:product_id>/', delete_product, name='delete-product'),
]