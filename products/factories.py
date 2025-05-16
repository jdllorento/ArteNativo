import factory
from faker import Faker
import random
from decimal import Decimal

from .models import Category, Product, Review
from users.factories import UserFactory # Import UserFactory

fake = Faker()


PLACEHOLDER_IMAGES = [
    'products/default.jpg',
]

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Faker('word')

class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    rating = factory.Faker('random_int', min=1, max=5)
    comment = factory.Faker('paragraph', nb_sentences=2)

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('catch_phrase')
    description = factory.Faker('paragraph', nb_sentences=3)
    stock = factory.Faker('random_int', min=0, max=200)
    price = factory.LazyAttribute(lambda o: Decimal(fake.random_int(min=10, max=10000)) / Decimal(100))
    
    image = factory.LazyAttribute(lambda o: random.choice(PLACEHOLDER_IMAGES))
     
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def create_reviews_for_product(obj, create, extracted, **kwargs):
        """Create a random number of reviews for this product."""
        if not create:
            # Simple build, do nothing.
            return

        num_reviews = random.randint(0, 5)
        for _ in range(num_reviews):
            ReviewFactory.create(product=obj)