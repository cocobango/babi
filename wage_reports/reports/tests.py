from decimal import *
getcontext().prec = 6
import json

from django.test import TestCase
from django.utils import timezone

from reports.models import Employer , Employee , Monthly_employee_data , Monthly_employer_data , Monthly_system_data
from django.contrib.auth.models import User
from . import factories , helpers , reports_maker

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


class HelpersTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(HelpersTestCase, self).__init__(*args,**kwargs)
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
            [Decimal(247.8) * 1, helpers.calculate_income_tax(overall_gross=7000,income_tax_threshold=15000,lower_tax_threshold=0.05,upper_tax_threshold=0.2,is_required_to_pay_income_tax=True,exact_income_tax_percentage=0.03,accumulated_gross_including_this_month=9000,accumulated_income_tax_not_including_this_month=1000,vat_due_this_month=1260)],
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
        social_security_employee = helpers.calculate_social_security_employee(overall_gross=overall_gross,social_security_threshold=5500,lower_employee_social_security_percentage=0.035,upper_employee_social_security_percentage=0.12,is_required_to_pay_social_security=True, is_employer_the_main_employer=False, gross_payment_from_others=2000)
        income_tax = helpers.calculate_income_tax(overall_gross=overall_gross,income_tax_threshold=15000,lower_tax_threshold=0.05,upper_tax_threshold=0.2,is_required_to_pay_income_tax=True,exact_income_tax_percentage=0,accumulated_gross_including_this_month=9000,accumulated_income_tax_not_including_this_month=200,vat_due_this_month=output_tax)
        #act
        test_set=[
            # basic threshold calculation
            [ Decimal(7467.50)*1 , helpers.calculate_monthly_net(overall_gross,output_tax,social_security_employee['total'],income_tax)],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

class CalculationTestCase(object):
    def __init__(self,*args, **kwargs):
        super(CalculationTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
    def setUp(self):
        self.myGenerator.generateInitialControlledState()


    def test_data_from_setup_is_present(self):
        #arrange
        monthly_employee_data = Monthly_employee_data.objects.get(employee=1,for_month=1, for_year=2015, is_approved=True)
        #act
        gross_payment = monthly_employee_data.gross_payment

        #assert
        self.assertEqual(5000, gross_payment)



class ReportsTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(ReportsTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
    def setUp(self):
        self.myGenerator.generateInitialControlledState()
        first_employer = Employer.objects.order_by('-id')[0]
        self.reports_maker = reports_maker.ReportsMaker(employer=first_employer)

    def test_reports_of_all_types_exists(self):
        pass
        # print(self.reports_maker.monthly_employee_report(employee=1,for_year=2015, for_month=1))
        # print(self.reports_maker.monthly_employer_report(employer=1,for_year=2015, for_month=1))
        # print(self.reports_maker.three_months_employer_report(employer=1,for_year=2015, for_month=1))
        # print(self.reports_maker.yearly_employee_report(employee=1,for_year=2015))
        # print(self.reports_maker.yearly_social_security_employer_report(employer=1, for_year=2015))

        # #856 report
        # print(self.reports_maker.yearly_income_tax_employer_report(employer=1, for_year=2015))

    def test_data_from_setup_is_present(self):
        #arrange
        first_employee = Employee.objects.order_by('id')[0]
        monthly_employee_data = Monthly_employee_data.objects.get(employee=first_employee,for_month=1, for_year=2015, is_approved=True)
        #act
        gross_payment = monthly_employee_data.gross_payment

        #assert
        self.assertEqual(5000, gross_payment)

    def test_monthly_employee_report_has_all_fields(self):
        #arrange
        fields = [
            'salary',
            'general_expenses',
            'income_tax_due_this_month',
            'social_security_employee_due_this_month',
            'vat_due_this_month',
            'monthly_net'
        ]
        first_employee = Employee.objects.order_by('id')[0]
        #act
        monthly_employee_report = self.reports_maker.monthly_employee_report(employee=first_employee,for_year=2015, for_month=1)
        #assert
        for field in fields:
            self.assertIn(field , monthly_employee_report)
        # print(monthly_employee_report)

    def test_correctly_caclutates_income_tax(self):
        monthly_reports_for_january = self.generate_monthly_reports_bulk(for_month=1)

        test_set=[
            # does not have to pay tax
            [ 0 , monthly_reports_for_january[0]['income_tax_due_this_month'] ],
            [ Decimal(413)*1 , monthly_reports_for_january[1]['income_tax_due_this_month'] ],
            [ Decimal(250)*1 , monthly_reports_for_january[2]['income_tax_due_this_month'] ],
            [ Decimal(140)*1 , monthly_reports_for_january[3]['income_tax_due_this_month'] ],
            [ Decimal(283.2)*1 , monthly_reports_for_january[4]['income_tax_due_this_month'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_social_security(self):
        monthly_reports_for_january = self.generate_monthly_reports_bulk(for_month=1)

        test_set=[
            [ Decimal(175)*1 , monthly_reports_for_january[0]['social_security_employee_due_this_month'] ],
            [ Decimal(840)*1 , monthly_reports_for_january[1]['social_security_employee_due_this_month'] ],
            [ Decimal(0)*1 , monthly_reports_for_january[2]['social_security_employee_due_this_month'] ],
            [ Decimal(262.74)*1 , monthly_reports_for_january[3]['social_security_employee_due_this_month'] ],
            [ Decimal(960)*1 , monthly_reports_for_january[4]['social_security_employee_due_this_month'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_vat(self):
        monthly_reports_for_january = self.generate_monthly_reports_bulk(for_month=1)

        test_set=[
            [ Decimal(900)*1 , monthly_reports_for_january[0]['vat_due_this_month'] ],
            [ Decimal(1260)*1 , monthly_reports_for_january[1]['vat_due_this_month'] ],
            [ Decimal(0)*1 , monthly_reports_for_january[2]['vat_due_this_month'] ],
            [ Decimal(0)*1 , monthly_reports_for_january[3]['vat_due_this_month'] ],
            [ Decimal(1440)*1 , monthly_reports_for_january[4]['vat_due_this_month'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_monthly_net_january(self):
        monthly_reports_for_january = self.generate_monthly_reports_bulk(for_month=1)

        test_set=[
            [ Decimal(5725)*1 , monthly_reports_for_january[0]['monthly_net'] ],
            [ Decimal(7007)*1 , monthly_reports_for_january[1]['monthly_net'] ],
            [ Decimal(2250)*1 , monthly_reports_for_january[2]['monthly_net'] ],
            [ Decimal(3597.26)*1 , monthly_reports_for_january[3]['monthly_net'] ],
            [ Decimal(8196.8)*1 , monthly_reports_for_january[4]['monthly_net'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_monthly_net_february(self):
        monthly_reports_for_february = self.generate_monthly_reports_bulk(for_month=2)

        test_set=[
            [ Decimal(5725)*1 , monthly_reports_for_february[0]['monthly_net'] ],
            [ Decimal(6006)*1 , monthly_reports_for_february[1]['monthly_net'] ],
            [ Decimal(5152.26)*1 , monthly_reports_for_february[2]['monthly_net'] ],
            [ Decimal(0)*1 , monthly_reports_for_february[3]['monthly_net'] ],
            [ Decimal(4098.40)*1 , monthly_reports_for_february[4]['monthly_net'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_monthly_net_march(self):
        # for month in Monthly_employer_data.objects.filter(for_year=2015,for_month=3, is_approved=True):
        #     print(month.id)
        #     print(month.employee)
        #     print(month.is_required_to_pay_income_tax)

        monthly_reports_for_march = self.generate_monthly_reports_bulk(for_month=3)
        # print(monthly_reports_for_march[3])

        test_set=[
            [ Decimal(5725)*1 , monthly_reports_for_march[0]['monthly_net'] ],
            [ Decimal(5830)*1 , monthly_reports_for_march[1]['monthly_net'] ],
            [ Decimal(3325)*1 , monthly_reports_for_march[2]['monthly_net'] ],
            [ Decimal(3330)*1 , monthly_reports_for_march[3]['monthly_net'] ],
            [ Decimal(6147.6)*1 , monthly_reports_for_march[4]['monthly_net'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])



    def generate_monthly_reports_bulk(self, for_month):
        employees = Employee.objects.all()

        monthly_employee_reports = []
        for employee in employees:
            monthly_employee_reports.append(self.reports_maker.monthly_employee_report(employee=employee,for_year=2015, for_month=for_month))
        return monthly_employee_reports
        

class ValidationTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(ValidationTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
    def setUp(self):
        pass

    
