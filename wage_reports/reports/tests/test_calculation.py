from .tests_imports import * 

class CalculationTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(CalculationTestCase, self).__init__(*args,**kwargs)
        employer = Employer.objects.order_by('-id')[0]
        self.myGenerator = factories.MyGenerators()
        self.data_getter = data_getter()
        self.income_tax = income_tax_calculations(user_id=employer.user.id)
        self.social_security = social_security_calculations(user_id=employer.user.id)
        self.vat = vat_calculations(user_id=employer.user.id)
        self.cross = cross_calculations(user_id=employer.user.id)

    def setUp(self):
        self.myGenerator.generateInitialControlledState()
        first_employer = Employer.objects.order_by('-id')[0]
        self.reports_maker = reports_maker.ReportsMaker(employer=first_employer)


    def test_data_from_setup_is_present(self):
        #arrange
        employee = Employee.objects.order_by('id')[0]
        monthly_employee_data = Monthly_employee_data.objects.get(employee=employee,for_month=1, for_year=2015, is_approved=True)
        #act
        gross_payment = monthly_employee_data.gross_payment

        #assert
        self.assertEqual(5000, gross_payment)


    def test_correctly_inserts_monthly_report_data_income_tax(self): 
        #arrange
        employee = Employee.objects.order_by('id')[1]
        monthly_employee_report_to_db = self.cross.monthly_employee_report_to_db(employee=employee, for_year=2015, for_month=1)
        #act
        monthly_employee_report_data = Monthly_employee_report_data.objects.get(employee=employee,for_month=1, for_year=2015)
        
        #assert
        self.assertEqual(413, monthly_employee_report_data.income_tax)

    def test_correctly_inserts_monthly_social_security_report_data(self):  
        #arrange
        employee = Employee.objects.order_by('id')[1]
        self.cross.monthly_employee_report_to_db(employee=employee, for_year=2015, for_month=1)
        
        #act
        monthly_employee_social_security_report_data = Monthly_employee_social_security_report_data.objects.select_related('monthly_employee_report_data').get(monthly_employee_report_data__employee=employee,monthly_employee_report_data__for_month=1, monthly_employee_report_data__for_year=2015) 
        
        #assert
        self.assertEqual(840, monthly_employee_social_security_report_data.total)
