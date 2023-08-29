# Allegro Scrapper

**Latest update:** August 29, 2023

Welcome to the Allegro Scrapper project!

## Overview

This project serves as a simple tool for quickly checking product prices based on their **EAN** numbers. Additionally, the app collects various data points for a given EAN, providing insights into how the product is performing on Allegro.

## About the Project

The Allegro Scrapper is built using the Django framework and Selenium libraries in Python. It's designed as a backend application that can be hosted on a server to provide APIs and serve data on web pages.

## App URLs

- `/`: The index.html page displays a table of all items found in the database.
- `/delete-product/<int:product_id>`: Deletes a product by its ID.
- `/run-scraper/<str:ean>`: Initiates the Selenium script with the provided EAN.

## How It Works

1. Accessing the `/run-scraper/{ean}` URL triggers the `run_scrapper` function in the Django views.
2. Selenium operations are performed in the `main.py` script.
3. After data is collected, it's returned to Django and saved in the database.
4. The page is refreshed, showing the new record in the table.

## Key Points

- Randomization is implemented at every step to reduce detection risks.
- Two drivers can be used: an undetected one or a normal Selenium Chrome driver with randomized user agents.
- If Django is not needed, you can use the `Selenium` folder independently, though data saving would need to be handled externally.
- Some table cells in `index.html` might truncate text due to length. You can adjust this, but be aware of the "Copy" button to copy full cell data.

## Django Superuser Access

- **Login**: admin
- **Password**: admin

You can create your own superuser with the command **python manage.py createsuperuser**.

## Potential Errors

- Allegro might detect the bot; you can reduce detection by running `driver_init` with `run_undetected = True`.
- Ensure that you have the correct version of `chromedriver.exe` for your browser.
- If data gathering encounters issues, check the console and ensure that Selenium is targeting the proper classes.

Happy Hacking! 🕵🏻