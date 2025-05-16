import factory
from faker import Faker
from django.contrib.auth.hashers import make_password
from .models import User

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda o: f'{o.first_name.lower()}.{o.last_name.lower()}{fake.random_int(min=1, max=99)}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    password = factory.LazyFunction(lambda: make_password('defaultpassword123'))
    is_staff = False
    is_active = True
    is_superuser = False

    # Custom fields
    role = factory.Iterator([User.CUSTOMER, User.ADMIN])
    address = factory.Faker('address')
    document_type = factory.Iterator([choice[0] for choice in User._meta.get_field('document_type').choices if choice[0]])
    document_number = factory.Faker('ssn')

    @factory.post_generation
    def set_group(self, create, extracted, **kwargs):
        if self.role == User.ADMIN:
            self.is_staff = True
            self.is_superuser = True
            self.save() 