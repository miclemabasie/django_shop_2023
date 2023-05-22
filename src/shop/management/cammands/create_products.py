from django.core.management.base import BaseCommand
from shop.models import Product
import datetime


class Command(BaseCommand):
    help = "Adds products to the database"

    def handle(self, *args, **options):
        products = [
            {
                "name": "MacBook Pro",
                "slug": "macbook-pro",
                "image": "https://example.com/images/macbook-pro.jpg",
                "description": "Apple MacBook Pro laptop",
                "price": 1499.99,
                "available": True,
                "created": datetime.datetime.now(),
                "updated": datetime.datetime.now(),
            },
            {
                "name": "iPhone X",
                "slug": "iphone-x",
                "image": "https://example.com/images/iphone-x.jpg",
                "description": "Apple iPhone X smartphone",
                "price": 799.99,
                "available": True,
                "created": datetime.datetime.now(),
                "updated": datetime.datetime.now(),
            },
            # Add more products here...
        ]

        for product_data in products:
            product = Product(**product_data)
            product.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully added "{product.name}" to the database'
                )
            )
