from .tests_imports import * 

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
        self.assertEqual(296 , response['total_employer'])

    def test_social_security_employee_with_upper_percentage(self):
        #arrange
        #act
        response = helpers.calculate_social_security_employee(overall_gross=7000,social_security_threshold=5500,lower_employee_social_security_percentage=0.033,upper_employee_social_security_percentage=0.12,is_required_to_pay_social_security=True, is_employer_the_main_employer=False, gross_payment_from_others=2000)
        #assert
        self.assertEqual(535.5 , response['total_employee'])

    def test_social_security_employee_without_upper_percentage(self):
        #arrange
        #act
        response = helpers.calculate_social_security_employee(overall_gross=7000,social_security_threshold=5500,lower_employee_social_security_percentage=0.033,upper_employee_social_security_percentage=0.12,is_required_to_pay_social_security=True, is_employer_the_main_employer=True, gross_payment_from_others=2000)
        #assert
        self.assertEqual(361.5 , response['total_employee'])


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
            [ Decimal(7467.50)*1 , helpers.calculate_monthly_net(overall_gross,output_tax,social_security_employee['total_employee'],income_tax)],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])