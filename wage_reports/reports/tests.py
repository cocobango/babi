from decimal import *
import json

from django.test import TestCase
from django.utils import timezone

from reports.models import Employer , Employee , Monthly_employee_data , Monthly_employer_data , Monthly_system_data
from django.contrib.auth.models import User
from . import factories
from . import helpers

class SetupTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(SetupTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
        print('running setup test case')
    def setUp(self):
        pass
    def test_tests_are_realy_running(self):
        """test realy run"""
        self.assertTrue(True)

    def test_able_to_create_a_user_with_factory(self):
        #arrange
        employer = factories.EmployerFactory()

        #act
        latest_employer = Employer.objects.order_by('-id')[0]
        
        #assert
        self.assertEqual(employer.id , latest_employer.id)
        self.assertEqual(employer.user.id , latest_employer.user.id)


    def test_able_to_create_an_employee_with_factory(self):
        #arrange
        employee = factories.EmployeeFactory()

        #act
        latest_employee = Employee.objects.order_by('-id')[0]

        #assert
        self.assertEqual(employee.id , latest_employee.id)
        self.assertEqual(employee.user.id , latest_employee.user.id)

    def test_employee_belongs_to_employer(self):
        #arrange
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)
        #act
        #assert
        self.assertEqual(employee.employer.id , employer.id)

    def test_able_to_generate_multiple_employees_for_the_same_employer(self):
        #arrange
        employer = factories.EmployerFactory()
        
        #act
        employee_1 = factories.EmployeeFactory(employer=employer)
        employee_2 = factories.EmployeeFactory(employer=employer)
        employee_3 = factories.EmployeeFactory(employer=employer)

        #assert
        self.assertEqual(employee_1.employer.id , employer.id)
        self.assertEqual(employee_2.employer.id , employer.id)
        self.assertEqual(employee_3.employer.id , employer.id)


    def test_able_to_insert_monthly_employer_data(self):
        #arrange
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)  

        #act
        monthly_employer_data = Monthly_employer_data.objects.create(employee=employee ,
            created = timezone.now(),
            entered_by = 'admin',
            is_approved = True,
            for_year = 0,
            for_month = 0,
            is_required_to_pay_vat = True,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = Decimal(0.05),
            upper_tax_threshold = Decimal(0.1),
            income_tax_threshold = Decimal(60000),
            exact_income_tax_percentage = Decimal(0.15) 
        )  

        #assert
        self.assertIsInstance(monthly_employer_data.id , int)
        self.assertEqual(monthly_employer_data.employee.id , employee.id)


    def test_able_to_insert_monthly_employer_data_with_factory(self):
        #arrange
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)  

        #act
        monthly_employer_data = factories.MonthlyEmployerDataFactory(employee=employee)  

        #assert
        self.assertIsInstance(monthly_employer_data.id , int)
        self.assertEqual(monthly_employer_data.employee.id , employee.id)

    def test_able_to_use_my_generators_class(self):
        self.assertTrue(self.myGenerator.stub())


    def test_able_to_insert_monthly_employee_data_with_generator(self):
        #arrange
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)  
        employeeData = {
            'employee' : employee,
        }
        #act
        monthly_employee_data = self.myGenerator.generateMonthlyEmployeeDataWithFactory(employeeData=employeeData)  

        #assert
        self.assertIsInstance(monthly_employee_data.id , int)
        self.assertEqual(monthly_employee_data.employee.id , employee.id)

    def test_able_to_explicitly_set_attribute_to_monthly_employee_data(self):
        #arrange
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)  
        employeeData = {
            'employee' : employee,
            'salary' : 2000
        }
        #act
        monthly_employee_data = self.myGenerator.generateMonthlyEmployeeDataWithFactory(employeeData=employeeData)  

        #assert
        self.assertEqual(monthly_employee_data.salary , 2000)

    def test_able_to_insert_monthly_system_data(self):
        #arrange

        #act
        monthly_system_data = factories.MonthlySystemDataFactory()

        #assert
        self.assertIsInstance(monthly_system_data.id , int)


class CalculationTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(CalculationTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
    def setUp(self):
        print('doing some setup')

    def test_social_security_employer(self):
        #arrange
        #act
        response = helpers.calculate_social_security_employer(overall_gross=7000,social_security_threshold=5500,lower_employer_social_security_percentage=Decimal(0.035),upper_employer_social_security_percentage=Decimal(0.069),is_required_to_pay_social_security=True)
        #assert
        self.assertEqual(296 , response['total'])

    def test_social_security_employee_with_upper_percentage(self):
        #arrange
        #act
        response = helpers.calculate_social_security_employee(overall_gross=7000,social_security_threshold=5500,lower_employee_social_security_percentage=0.033,upper_employee_social_security_percentage=0.12,is_required_to_pay_social_security=True, is_employer_the_main_employer=False, gross_payment_from_others=2000)
        #assert
        self.assertEqual(535.5 , response['total'])

    def test_social_security_employee_without_upper_percentage(self):
        #arrange
        #act
        response = helpers.calculate_social_security_employee(overall_gross=7000,social_security_threshold=5500,lower_employee_social_security_percentage=0.033,upper_employee_social_security_percentage=0.12,is_required_to_pay_social_security=True, is_employer_the_main_employer=True, gross_payment_from_others=2000)
        #assert
        self.assertEqual(361.5 , response['total'])


    #@todo third and second assertions are wrong.
    def test_income_tax(self):
        #arrange
        test_set=[
            # basic threshold calculation
            [ 250 , helpers.calculate_income_tax(overall_gross=7000,income_tax_threshold=15000,lower_tax_threshold=0.05,upper_tax_threshold=0.2,is_required_to_pay_income_tax=True,exact_income_tax_percentage=0,accumulated_gross_including_this_month=9000,accumulated_income_tax_not_including_this_month=200,vat_due_this_month=0)],
            # expecting tax refund
            [-550, helpers.calculate_income_tax(overall_gross=7000,income_tax_threshold=15000,lower_tax_threshold=0.05,upper_tax_threshold=0.2,is_required_to_pay_income_tax=True,exact_income_tax_percentage=0,accumulated_gross_including_this_month=9000,accumulated_income_tax_not_including_this_month=1000,vat_due_this_month=0)],
            # fix income tax without vat
            [210, helpers.calculate_income_tax(overall_gross=7000,income_tax_threshold=15000,lower_tax_threshold=0.05,upper_tax_threshold=0.2,is_required_to_pay_income_tax=True,exact_income_tax_percentage=0.03,accumulated_gross_including_this_month=9000,accumulated_income_tax_not_including_this_month=1000,vat_due_this_month=0)],
            # fix income tax with vat
            [248, helpers.calculate_income_tax(overall_gross=7000,income_tax_threshold=15000,lower_tax_threshold=0.05,upper_tax_threshold=0.2,is_required_to_pay_income_tax=True,exact_income_tax_percentage=0.03,accumulated_gross_including_this_month=9000,accumulated_income_tax_not_including_this_month=1000,vat_due_this_month=1260)],
        ]
        #act
        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_output_tax(self):
        #arrange
        test_set=[
            # basic threshold calculation
            [ 1260 , helpers.calculate_output_tax(overall_gross=7000,vat_percentage=0.18,is_required_to_pay_vat=True)],
        ]

        #act
        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    #@todo assertion is wrong.
    def test_monthly_net(self):
        #arrange
        overall_gross = 7000
        output_tax = helpers.calculate_output_tax(overall_gross=overall_gross,vat_percentage=0.18,is_required_to_pay_vat=True)
        social_security_employee = helpers.calculate_social_security_employee(overall_gross=overall_gross,social_security_threshold=5500,lower_employee_social_security_percentage=0.033,upper_employee_social_security_percentage=0.12,is_required_to_pay_social_security=True, is_employer_the_main_employer=False, gross_payment_from_others=2000)
        income_tax = helpers.calculate_income_tax(overall_gross=overall_gross,income_tax_threshold=15000,lower_tax_threshold=0.05,upper_tax_threshold=0.2,is_required_to_pay_income_tax=True,exact_income_tax_percentage=0,accumulated_gross_including_this_month=9000,accumulated_income_tax_not_including_this_month=200,vat_due_this_month=output_tax)
        #act
        test_set=[
            # basic threshold calculation
            [ 1260 , helpers.calculate_monthly_net(overall_gross,output_tax,social_security_employee['total'],income_tax)],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
