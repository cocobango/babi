from decimal import *

from django.test import TestCase
from django.utils import timezone

from reports.models import Employer , Employee , Monthly_employee_data , Monthly_employer_data
from django.contrib.auth.models import User
from . import factories

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



class CalculationTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(CalculationTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
    def setUp(self):
        print('doing some setup')
    def test_tests_are_realy_running(self):
        """test realy run"""
        self.assertTrue(True)
