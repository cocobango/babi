from decimal import *

from django.utils import timezone

import factory
from . import models

from faker import Faker
import random

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
    password = factory.PostGenerationMethodCall('set_password',
                                                '123456')
    username = factory.Sequence(lambda n: 'john%s' % n)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    first_name = 'john'
    last_name = fake.name()


class EmployerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Employer
    user = factory.SubFactory(UserFactory)
    is_required_to_pay_vat = True
    is_npo = False
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

class MonthlyEmployerDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Monthly_employer_data 
    employee = factory.SubFactory(EmployeeFactory)
    created = timezone.now()
    entered_by = 'admin'
    is_approved = True
    for_year = 0
    for_month = 0
    is_required_to_pay_vat = True
    is_required_to_pay_income_tax = True
    lower_tax_threshold = Decimal(0.05)
    upper_tax_threshold = Decimal(0.1)
    income_tax_threshold = Decimal(60000)
    exact_income_tax_percentage = Decimal(0.15)
    gross_or_cost = True

class MonthlyEmployeeDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Monthly_employee_data 
    employee = factory.SubFactory(EmployeeFactory)
    created = timezone.now()
    entered_by = 'admin'
    is_approved = True
    gross_payment = Decimal(1000)
    salary = Decimal(900)
    general_expenses = Decimal(100)
    is_required_to_pay_social_security = True
    is_employer_the_main_employer = False
    gross_payment_from_others = Decimal(200)
    for_year = 0
    for_month = 0

class MonthlySystemDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Monthly_system_data 
    created = timezone.now()
    for_year = 0
    for_month = 0
    vat_percentage = Decimal(0.17)
    social_security_threshold = 70000
    lower_employee_social_security_percentage = Decimal(0.07)
    lower_employer_social_security_percentage = Decimal(0.1)
    upper_employee_social_security_percentage = Decimal(0.12)
    upper_employer_social_security_percentage = Decimal(0.14)
    maximal_sum_to_pay_social_security = 100000
    lower_health_insurance_percentage = Decimal(0.031)
    upper_health_insurance_percentage = Decimal(0.05)
    income_tax_default = Decimal(0.3)


class MyGenerators(object):
    """Functions that assist in creating factories that handle the constraints in my models' ".save()" method"""
    def __init__(self):
        super(MyGenerators, self).__init__()
    
    def stub(self):
        return True

    def generateMonthlyEmployeeDataWithFactory(self, *args, **kwargs):
        """I have to make sure a user has employer data before inserting employee data. 
        After I do that, I use the kwargs given to create the monthly data objects"""
        employeeData = kwargs.get('employeeData',{})
        employerData = kwargs.get('employerData',{})
        
        if 'employee' not in employeeData:
            return False
        
        if 'employee' not in employerData:
            employerData['employee'] = employeeData['employee']
        
        try:
            employerDataFromDb = models.Monthly_employer_data.objects.filter(employee=employeeData['employee'], is_approved=True)[0]
        except IndexError as e:
            MonthlyEmployerDataFactory(**employerData)
        
        return MonthlyEmployeeDataFactory(**employeeData)

    def generate_monthly_system_data(self):
        monthly_system_data = MonthlySystemDataFactory(for_year = 2015,
            for_month = 1,
            vat_percentage = Decimal(0.18),
            social_security_threshold = 5556,
            lower_employee_social_security_percentage = Decimal(0.035),
            lower_employer_social_security_percentage = Decimal(0.0345),
            upper_employee_social_security_percentage = Decimal(0.12),
            upper_employer_social_security_percentage = Decimal(0.0725),
            maximal_sum_to_pay_social_security = 43240,
            income_tax_default = Decimal(0.48)
        )
        #duplicates months until august
        for x in range(2,13):
            monthly_system_data.for_month = x
            monthly_system_data.id = None
            monthly_system_data.save()

    def generateInitialControlledState(self):
        employer = EmployerFactory()
        employee_1 = EmployeeFactory(employer=employer)
        employee_2 = EmployeeFactory(employer=employer)
        employee_3 = EmployeeFactory(employer=employer)
        employee_4 = EmployeeFactory(employer=employer)
        employee_5 = EmployeeFactory(employer=employer)
        # user that does not have data in january
        employee_6 = EmployeeFactory(employer=employer)

        npo_employer = EmployerFactory(is_npo=True)
        employee_11 = EmployeeFactory(employer=npo_employer)
        employee_12 = EmployeeFactory(employer=npo_employer)
        employee_13 = EmployeeFactory(employer=npo_employer)
        employee_14 = EmployeeFactory(employer=npo_employer)
        employee_15 = EmployeeFactory(employer=npo_employer)
        # user that does not have data in january
        employee_16 = EmployeeFactory(employer=npo_employer)


        self.generate_monthly_system_data()

        #january
        MonthlyEmployerDataFactory(
            employee=employee_1,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = True,
            is_required_to_pay_income_tax = False,
            lower_tax_threshold = Decimal(0.05),
            upper_tax_threshold = Decimal(0.1),
            income_tax_threshold = Decimal(60000),
            exact_income_tax_percentage = Decimal(0.15)
        )
        MonthlyEmployeeDataFactory(
            employee=employee_1,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(5000),
            salary = Decimal(4500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = True,
            gross_payment_from_others = Decimal(1000)
        )

        MonthlyEmployerDataFactory(
            employee=employee_2,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = True,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = Decimal(0.05),
            upper_tax_threshold = Decimal(0.1),
            income_tax_threshold = Decimal(60000),
            exact_income_tax_percentage = Decimal(0.05)
        )
        MonthlyEmployeeDataFactory(
            employee=employee_2,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(7000),
            salary = Decimal(6500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )


        MonthlyEmployerDataFactory(
            employee=employee_3,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = False,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = Decimal(0.1),
            upper_tax_threshold = Decimal(0.21),
            income_tax_threshold = Decimal(10000),
            exact_income_tax_percentage = 0
        )
        MonthlyEmployeeDataFactory(
            employee=employee_3,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(2500),
            salary = Decimal(2000),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = False,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )


        MonthlyEmployerDataFactory(
            employee=employee_4,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = False,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = 0,
            upper_tax_threshold = Decimal(0.14),
            income_tax_threshold = Decimal(3000),
            exact_income_tax_percentage = 0
        )
        MonthlyEmployeeDataFactory(
            employee=employee_4,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(4000),
            salary = Decimal(3500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 3000
        )


        MonthlyEmployerDataFactory(
            employee=employee_5,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = True,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = Decimal(0.1),
            upper_tax_threshold = Decimal(0.21),
            income_tax_threshold = Decimal(10000),
            exact_income_tax_percentage = Decimal(0.03)
        )
        MonthlyEmployeeDataFactory(
            employee=employee_5,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(8000),
            salary = Decimal(7500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )


        #february
        MonthlyEmployeeDataFactory(
            employee=employee_1,
            for_year = 2015,
            for_month = 2,
            gross_payment = Decimal(5000),
            salary = Decimal(4500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = True,
            gross_payment_from_others = 1500
        )

        MonthlyEmployeeDataFactory(
            employee=employee_2,
            for_year = 2015,
            for_month = 2,
            gross_payment = Decimal(6000),
            salary = Decimal(5500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )

        MonthlyEmployeeDataFactory(
            employee=employee_3,
            for_year = 2015,
            for_month = 2,
            gross_payment = Decimal(6000),
            salary = Decimal(5500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = True,
            gross_payment_from_others = 0
        )


        

        MonthlyEmployeeDataFactory(
            employee=employee_5,
            for_year = 2015,
            for_month = 2,
            gross_payment = Decimal(4000),
            salary = Decimal(3500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )


        MonthlyEmployerDataFactory(
            employee=employee_6,
            for_year = 2015,
            for_month = 2,
            is_required_to_pay_vat = False,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = 0,
            upper_tax_threshold = Decimal(0.14),
            income_tax_threshold = Decimal(7000),
            exact_income_tax_percentage = 0
        )
        MonthlyEmployeeDataFactory(
            employee=employee_6,
            for_year = 2015,
            for_month = 2,
            gross_payment = Decimal(4500),
            salary = Decimal(4000),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = Decimal(2000)
        )

        #march
        MonthlyEmployeeDataFactory(
            employee=employee_1,
            for_year = 2015,
            for_month = 3,
            gross_payment = Decimal(5000),
            salary = Decimal(4500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = True,
            gross_payment_from_others = 2000
        )


        

        MonthlyEmployerDataFactory(
            employee=employee_2,
            for_year = 2015,
            for_month = 3,
            is_required_to_pay_vat = True,
            is_required_to_pay_income_tax = False,
            lower_tax_threshold = Decimal(0.05),
            upper_tax_threshold = Decimal(0.1),
            income_tax_threshold = Decimal(60000),
            exact_income_tax_percentage = Decimal(0.05)
        )


        MonthlyEmployeeDataFactory(
            employee=employee_2,
            for_year = 2015,
            for_month = 3,
            gross_payment = Decimal(5500),
            salary = Decimal(5000),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )


        MonthlyEmployeeDataFactory(
            employee=employee_3,
            for_year = 2015,
            for_month = 3,
            gross_payment = Decimal(4000),
            salary = Decimal(3500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = False,
            is_employer_the_main_employer = True,
            gross_payment_from_others = 0
        )


        MonthlyEmployeeDataFactory(
            employee=employee_4,
            for_year = 2015,
            for_month = 3,
            gross_payment = Decimal(4500),
            salary = Decimal(4000),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )


        MonthlyEmployeeDataFactory(
            employee=employee_5,
            for_year = 2015,
            for_month = 3,
            gross_payment = Decimal(6000),
            salary = Decimal(5500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )

        MonthlyEmployeeDataFactory(
            employee=employee_6,
            for_year = 2015,
            for_month = 3,
            gross_payment = Decimal(5000),
            salary = Decimal(4500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = Decimal(1000)
        )












            
        
        