import factory
from . import models

from faker import Faker
import random

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'john%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)


class EmployerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Employer
    user = factory.SubFactory(UserFactory)
    is_required_to_pay_vat = True
    business_id = random.randint(1000000,10000000)
    income_tax_id = random.randint(1000000,10000000)
    phone_number = random.randint(10000000,100000000)

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Employee
    user = factory.SubFactory(UserFactory)
    employer = factory.SubFactory(EmployerFactory)
    birthday = fake.simple_profile()['birthdate']
    government_id = random.randint(10000000,100000000)



    