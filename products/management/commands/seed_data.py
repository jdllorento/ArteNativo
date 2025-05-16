from django.core.management.base import BaseCommand
from django.db import transaction
from products.factories import ProductFactory, CategoryFactory
from users.factories import UserFactory

class Command(BaseCommand):
    help = 'Seeds the database with products, categories, users, and reviews.'

    def add_arguments(self, parser):
        parser.add_argument('--products', type=int, default=20, help='Number of products to create.')
        parser.add_argument('--users', type=int, default=10, help='Number of unique users to create.')
        parser.add_argument('--categories', type=int, default=5, help='Number of unique categories to create.')

    @transaction.atomic
    def handle(self, *args, **options):
        num_products = options['products']
        num_users = options['users']
        num_categories = options['categories']

        self.stdout.write(self.style.SUCCESS(f'Seeding database...'))

        # Create Users
        users = UserFactory.create_batch(num_users)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(users)} users.'))

        # Create Categories
        categories = CategoryFactory.create_batch(num_categories)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(categories)} categories.'))

        # Create Products
        products = []
        for _ in range(num_products):
            product = ProductFactory.create()
            products.append(product)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(products)} products.'))
        
        total_reviews = sum(product.reviews.count() for product in products)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_reviews} reviews across all products.'))

        self.stdout.write(self.style.SUCCESS(f'Database seeding complete!')) 