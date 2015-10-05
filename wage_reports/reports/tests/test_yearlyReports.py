from .tests_imports import * 

class YearlyReportsTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(YearlyReportsTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
    def setUp(self):
        self.myGenerator.generateInitialControlledState()
        first_employer = Employer.objects.order_by('-id')[0]
        self.reports_maker = reports_maker.ReportsMaker(employer=first_employer)
        populate_db_with_the_results_of_calculations_for_all_months()



	#yearly_employee_report suite
    def test_yearly_employee_report_has_all_fields(self):
        #arrange 
        fields = [
            'first_name',
            'last_name',
            'government_id',
            'months_in_which_got_paid',
            'sum_of_income_tax',
            'sum_of_social_security',
            'sum_of_vat',
            'sum_of_gross_payment',
        ]
        first_employee = Employee.objects.order_by('id')[0]

        #act
        yearly_employee_report = self.reports_maker.yearly_employee_report(employee=first_employee , for_year=2015)

        # print(yearly_employee_report)
        #assert
        for field in fields:
            self.assertIn(field , yearly_employee_report)
        # print(monthly_employee_report)

    def test_correctly_caclutates_yearly_employee_report_first_employee(self):
        #arange
        first_employee = Employee.objects.order_by('id')[0]

        #act
        yearly_employee_report = self.reports_maker.yearly_employee_report(employee=first_employee , for_year=2015)

        #assert
        test_set=[
            # does not have to pay tax
            [ Decimal(15000)*1 , yearly_employee_report['sum_of_gross_payment'] ],
            [ Decimal(0)*1 , yearly_employee_report['sum_of_income_tax'] ],
            [ Decimal(525)*1 , yearly_employee_report['sum_of_social_security'] ],
            [ Decimal(2700)*1 , yearly_employee_report['sum_of_vat'] ],
            [ [1,2,3] , yearly_employee_report['months_in_which_got_paid'] ],
        ]

        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_yearly_employee_report_second_employee(self):
        #arange
        second_employee = Employee.objects.order_by('id')[1]

        #act
        yearly_employee_report = self.reports_maker.yearly_employee_report(employee=second_employee , for_year=2015)

        #assert
        test_set=[
            # does not have to pay tax
            [ Decimal(18500)*1 , yearly_employee_report['sum_of_gross_payment'] ],
            [ Decimal(767)*1 , yearly_employee_report['sum_of_income_tax'] ],
            [ Decimal(2220)*1 , yearly_employee_report['sum_of_social_security'] ],
            [ Decimal(3330)*1 , yearly_employee_report['sum_of_vat'] ],
            [ [1,2,3] , yearly_employee_report['months_in_which_got_paid'] ],
        ]

        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_yearly_employee_report_third_employee(self):
        #arange
        employee = Employee.objects.order_by('id')[2]

        #act
        yearly_employee_report = self.reports_maker.yearly_employee_report(employee=employee , for_year=2015)

        #assert
        test_set=[
            # does not have to pay tax
            [ Decimal(12500)*1 , yearly_employee_report['sum_of_gross_payment'] ],
            [ Decimal(1525)*1 , yearly_employee_report['sum_of_income_tax'] ],
            [ Decimal(247.74)*1 , yearly_employee_report['sum_of_social_security'] ],
            [ Decimal(0)*1 , yearly_employee_report['sum_of_vat'] ],
            [ [1,2,3] , yearly_employee_report['months_in_which_got_paid'] ],
        ]

        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_yearly_employee_report_forth_employee(self):
        #arange
        employee = Employee.objects.order_by('id')[3]

        #act
        yearly_employee_report = self.reports_maker.yearly_employee_report(employee=employee , for_year=2015)

        #assert
        test_set=[
            # does not have to pay tax
            [ Decimal(8500)*1 , yearly_employee_report['sum_of_gross_payment'] ],
            [ Decimal(770)*1 , yearly_employee_report['sum_of_income_tax'] ],
            [ Decimal(802.74)*1 , yearly_employee_report['sum_of_social_security'] ],
            [ Decimal(0)*1 , yearly_employee_report['sum_of_vat'] ],
            [ [1,3] , yearly_employee_report['months_in_which_got_paid'] ],
        ]

        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
    
    def test_correctly_caclutates_yearly_employee_report_fifth_employee(self):
        #arange
        employee = Employee.objects.order_by('id')[4]

        #act
        yearly_employee_report = self.reports_maker.yearly_employee_report(employee=employee , for_year=2015)

        #assert
        test_set=[
            # does not have to pay tax
            [ Decimal(18000)*1 , yearly_employee_report['sum_of_gross_payment'] ],
            [ Decimal(637.2)*1 , yearly_employee_report['sum_of_income_tax'] ],
            [ Decimal(2160)*1 , yearly_employee_report['sum_of_social_security'] ],
            [ Decimal(3240)*1 , yearly_employee_report['sum_of_vat'] ],
            [ [1,2,3] , yearly_employee_report['months_in_which_got_paid'] ],
        ]

        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
   
    def test_correctly_caclutates_yearly_employee_report_sixth_employee(self):
        #arange
        employee = Employee.objects.order_by('id')[5]

        #act
        yearly_employee_report = self.reports_maker.yearly_employee_report(employee=employee , for_year=2015)

        #assert
        test_set=[
            # does not have to pay tax
            [ Decimal(9500)*1 , yearly_employee_report['sum_of_gross_payment'] ],
            [ Decimal(350)*1 , yearly_employee_report['sum_of_income_tax'] ],
            [ Decimal(450.48)*1 , yearly_employee_report['sum_of_social_security'] ],
            [ Decimal(0)*1 , yearly_employee_report['sum_of_vat'] ],
            [ [2,3] , yearly_employee_report['months_in_which_got_paid'] ],
        ]

        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])








    #yearly_income_tax_employer_report suite
    def test_yearly_income_tax_employer_report_has_all_fields(self):
        #arrange 
        employee_fields = [
            'first_name',
            'last_name',
            'government_id',
            'sum_of_income_tax',
            'sum_input_tax_vat',
            'sum_of_vat_and_gross_payment',
        ]
        outer_fields = [
            'income_tax_id',
            'sum_of_income_tax_from_all_employees',
            'sum_input_tax_vat_from_all_employees',
            'sum_of_vat_and_gross_payment_from_all_employees',
        ]
        first_employee = Employee.objects.order_by('id')[0]
        #act
        yearly_income_tax_employer_report = self.reports_maker.yearly_income_tax_employer_report(for_year=2015)

        #assert
        for field in employee_fields:
            self.assertIn(field , yearly_income_tax_employer_report['employees_list'][0])
        for field in outer_fields:
            self.assertIn(field , yearly_income_tax_employer_report)

    def test_correctly_caclutates_yearly_employee_report_first_employee(self):
        #arange
        
        #act
        yearly_income_tax_employer_report = self.reports_maker.yearly_income_tax_employer_report(for_year=2015)

        #assert
        test_set=[
            # does not have to pay tax
            [ Decimal(0)*1 , yearly_income_tax_employer_report['employees_list'][0]['sum_of_income_tax'] ],
            [ Decimal(767)*1 , yearly_income_tax_employer_report['employees_list'][1]['sum_of_income_tax'] ],
            [ Decimal(1525)*1 , yearly_income_tax_employer_report['employees_list'][2]['sum_of_income_tax'] ],
            [ Decimal(770)*1 , yearly_income_tax_employer_report['employees_list'][3]['sum_of_income_tax'] ],
            [ Decimal(637.2)*1 , yearly_income_tax_employer_report['employees_list'][4]['sum_of_income_tax'] ],
            [ Decimal(350)*1 , yearly_income_tax_employer_report['employees_list'][5]['sum_of_income_tax'] ]            
        ]

        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_yearly_employee_gross_payment_plus_vat(self):
        #arange
        gross_payment_plus_vat_arr = [Decimal(17700)*1, Decimal(21830)*1, Decimal(12500)*1, Decimal(8500)*1, Decimal(21240)*1, Decimal(9500)*1]

        #act
        yearly_income_tax_employer_report = self.reports_maker.yearly_income_tax_employer_report(for_year=2015)

        #assert
        for i in range(0,6):
            self.assertEqual(gross_payment_plus_vat_arr[i] , yearly_income_tax_employer_report['employees_list'][i]['sum_of_vat_and_gross_payment'])

    @unittest.skip("not implemented")
    def test_correctly_caclutates_yearly_employee_sum_input_tax_vat(self):
        #arange
        sum_input_tax_vat_arr = [Decimal(0)*1, Decimal(0)*1, Decimal(2250)*1, Decimal(1530)*1,  Decimal(0)*1, Decimal(1710)*1]

        #act
        yearly_income_tax_employer_report = self.reports_maker.yearly_income_tax_employer_report(for_year=2015)

        #assert
        for i in range(0,6):
            self.assertEqual(sum_input_tax_vat_arr[i] , yearly_income_tax_employer_report['employees_list'][i]['sum_input_tax_vat'])
    