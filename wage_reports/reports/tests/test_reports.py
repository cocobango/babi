from .tests_imports import * 

class ReportsTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(ReportsTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
    def setUp(self):
        self.myGenerator.generateInitialControlledState()
        populate_db_with_the_results_of_calculations_for_all_months()
        first_employer = Employer.objects.first()
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

    #monthly_employee_report suite
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
        monthly_reports_for_january = self.generate_monthly_employee_report_bulk(for_month=1)

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
        monthly_reports_for_january = self.generate_monthly_employee_report_bulk(for_month=1)

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
        monthly_reports_for_january = self.generate_monthly_employee_report_bulk(for_month=1)

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
        monthly_reports_for_january = self.generate_monthly_employee_report_bulk(for_month=1)

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
        monthly_reports_for_february = self.generate_monthly_employee_report_bulk(for_month=2)

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

        monthly_reports_for_march = self.generate_monthly_employee_report_bulk(for_month=3)
        # print(monthly_reports_for_march[3])

        test_set=[
            [ Decimal(5725)*1 , monthly_reports_for_march[0]['monthly_net'] ],
            [ Decimal(5830)*1 , monthly_reports_for_march[1]['monthly_net'] ],
            [ Decimal(3325)*1 , monthly_reports_for_march[2]['monthly_net'] ],
            [ Decimal(3330)*1 , monthly_reports_for_march[3]['monthly_net'] ],
            [ Decimal(6147.6)*1 , monthly_reports_for_march[4]['monthly_net'] ],
            [ Decimal(4437.26)*1 , monthly_reports_for_march[5]['monthly_net'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])



    def generate_monthly_employee_report_bulk(self, for_month):
        employees = Employee.objects.all()

        monthly_employee_reports = []
        for employee in employees:
            monthly_employee_reports.append(self.reports_maker.monthly_employee_report(employee=employee,for_year=2015, for_month=for_month))
        return monthly_employee_reports
    
    
                

    #monthly_employer_report suite
    def test_monthly_employer_report_has_all_social_security_fields(self):
        """ calculate social security for employer monthly report """
        #arrange
        social_security_fields = [
            'count_of_employees_that_are_required_to_pay_social_security',
            'sum_of_gross_payment_of_employees_that_are_required_to_pay_social_security',
            'sum_of_gross_payment_to_be_paid_at_lower_employer_rate_social_security',
            'sum_of_gross_payment_to_be_paid_at_lower_employee_rate_social_security',
            'total_of_social_security_due',
            'count_of_employees_that_do_not_exceed_the_social_security_threshold'
        ]
        #act
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #assert
        for field in social_security_fields:
            self.assertIn(field , monthly_employer_report['social_security'])
        # print(monthly_employee_report)


    def test_correctly_caclutates_social_security_in_monthly_employer_report_january(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #arrange + act
        test_set=[
            [ 4 , monthly_employer_report['social_security']['count_of_employees_that_are_required_to_pay_social_security'] ],
            [ 24000 , monthly_employer_report['social_security']['sum_of_gross_payment_of_employees_that_are_required_to_pay_social_security'] ],
            [ 20112 , monthly_employer_report['social_security']['sum_of_gross_payment_to_be_paid_at_lower_employer_rate_social_security'] ],
            [ 7556 , monthly_employer_report['social_security']['sum_of_gross_payment_to_be_paid_at_lower_employee_rate_social_security'] ],
            [ Decimal(3213.48)*1 , monthly_employer_report['social_security']['total_of_social_security_due'] ],
            [ 1 , monthly_employer_report['social_security']['count_of_employees_that_do_not_exceed_the_social_security_threshold'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_social_security_in_monthly_employer_report_february(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=2)
        #arrange + act
        test_set=[
            [ 5 , monthly_employer_report['social_security']['count_of_employees_that_are_required_to_pay_social_security'] ],
            [ 25500 , monthly_employer_report['social_security']['sum_of_gross_payment_of_employees_that_are_required_to_pay_social_security'] ],
            [ 24612 , monthly_employer_report['social_security']['sum_of_gross_payment_to_be_paid_at_lower_employer_rate_social_security'] ],
            [ 14112 , monthly_employer_report['social_security']['sum_of_gross_payment_to_be_paid_at_lower_employee_rate_social_security'] ],
            [ Decimal(2773.97)*1 , monthly_employer_report['social_security']['total_of_social_security_due'] ],
            [ 1 , monthly_employer_report['social_security']['count_of_employees_that_do_not_exceed_the_social_security_threshold'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
    def test_correctly_caclutates_social_security_in_monthly_employer_report_march(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=3)
        #arrange + act
        test_set=[
            [ 5 , monthly_employer_report['social_security']['count_of_employees_that_are_required_to_pay_social_security'] ],
            [ 26000 , monthly_employer_report['social_security']['sum_of_gross_payment_of_employees_that_are_required_to_pay_social_security'] ],
            [ 25556 , monthly_employer_report['social_security']['sum_of_gross_payment_to_be_paid_at_lower_employer_rate_social_security'] ],
            [ 9556 , monthly_employer_report['social_security']['sum_of_gross_payment_to_be_paid_at_lower_employee_rate_social_security'] ],
            [ Decimal(3221.61)*1 , monthly_employer_report['social_security']['total_of_social_security_due'] ],
            [ 1 , monthly_employer_report['social_security']['count_of_employees_that_do_not_exceed_the_social_security_threshold'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])





    @unittest.skip("not implemented")
    def test_monthly_employer_report_specific_waiting_to_be_resolved_march(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=3)
        #arrange + act
        test_set=[
            [ 1 , monthly_employer_report['social_security']['count_of_employees_that_do_not_exceed_the_social_security_threshold'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])




    def test_monthly_employer_report_has_all_vat_fields(self):
        """ calculate vat for employer monthly report """
        #arrange
        vat_fields = [
            'sum_of_gross_payment_where_no_vat_is_required',
            'count_of_employees_where_no_vat_is_required',
            'sum_of_vat_due_where_no_vat_is_required',
        ]
        #act
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #assert
        for field in vat_fields:
            self.assertIn(field , monthly_employer_report['vat'])
        # print(monthly_employee_report)


    def test_correctly_caclutates_vat_in_monthly_employer_report_january(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #arrange + act
        test_set=[
            [ Decimal(6500) * 1 , monthly_employer_report['vat']['sum_of_gross_payment_where_no_vat_is_required'] ],
            [ 2 , monthly_employer_report['vat']['count_of_employees_where_no_vat_is_required'] ],
            [ Decimal(1170) * 1 , monthly_employer_report['vat']['sum_of_vat_due_where_no_vat_is_required'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_vat_in_monthly_employer_report_february(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=2)
        #arrange + act
        test_set=[
            [ Decimal(10500) * 1 , monthly_employer_report['vat']['sum_of_gross_payment_where_no_vat_is_required'] ],
            [ 2 , monthly_employer_report['vat']['count_of_employees_where_no_vat_is_required'] ],
            [ Decimal(1890) * 1 , monthly_employer_report['vat']['sum_of_vat_due_where_no_vat_is_required'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
    def test_correctly_caclutates_vat_in_monthly_employer_report_march(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=3)
        #arrange + act
        test_set=[
            [ Decimal(13500) * 1 , monthly_employer_report['vat']['sum_of_gross_payment_where_no_vat_is_required'] ],
            [ 3 , monthly_employer_report['vat']['count_of_employees_where_no_vat_is_required'] ],
            [ Decimal(2430) * 1 , monthly_employer_report['vat']['sum_of_vat_due_where_no_vat_is_required'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_monthly_employer_report_has_all_income_tax_fields(self):
        """ calculate income tax for employer monthly report """
        #arrange
        income_tax_fields = [
            'count_of_employees_that_got_paid_this_month',
            'sum_of_gross_payment_and_vat_for_employees_that_got_paid_this_month',
            'sum_of_income_tax'
        ]
        #act
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #assert
        for field in income_tax_fields:
            self.assertIn(field , monthly_employer_report['income_tax'])
        # print(monthly_employee_report)


    def test_correctly_caclutates_income_tax_in_monthly_employer_report_january(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #arrange + act
        test_set=[
            [ 5 , monthly_employer_report['income_tax']['count_of_employees_that_got_paid_this_month'] ],
            [ Decimal(30100) * 1 , monthly_employer_report['income_tax']['sum_of_gross_payment_and_vat_for_employees_that_got_paid_this_month'] ],
            [ Decimal(1086.20) * 1 , monthly_employer_report['income_tax']['sum_of_income_tax'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_income_tax_in_monthly_employer_report_february(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=2)
        #arrange + act
        test_set=[
            [ 5 , monthly_employer_report['income_tax']['count_of_employees_that_got_paid_this_month'] ],
            [ Decimal(28200) * 1 , monthly_employer_report['income_tax']['sum_of_gross_payment_and_vat_for_employees_that_got_paid_this_month'] ],
            [ Decimal(1095.6) * 1 , monthly_employer_report['income_tax']['sum_of_income_tax'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
    def test_correctly_caclutates_income_tax_in_monthly_employer_report_march(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=3)
        #arrange + act
        test_set=[
            [ 6 , monthly_employer_report['income_tax']['count_of_employees_that_got_paid_this_month'] ],
            [ Decimal(32970) * 1 , monthly_employer_report['income_tax']['sum_of_gross_payment_and_vat_for_employees_that_got_paid_this_month'] ],
            [ Decimal(1867.40) * 1 , monthly_employer_report['income_tax']['sum_of_income_tax'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])


    def test_monthly_employer_report_has_all_book_keeping_where_no_vat_is_required_fields(self):
        """ calculate book keeping where no vat is required for employer monthly report """
        #arrange
        book_keeping_fields = [
            'sum_of_gross_payment_where_no_vat_is_required',
            'sum_of_employer_social_security_where_no_vat_is_required',
            'sum_of_net_payment_where_no_vat_is_required',
            'sum_of_income_tax_where_no_vat_is_required',
            'sum_of_social_security_where_no_vat_is_required',
            'list_of_names_and_monthly_net_where_no_vat_is_required',
            'sum_of_debits',
            'sum_of_credits'
        ]
        #act
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #assert
        for field in book_keeping_fields:
            self.assertIn(field , monthly_employer_report['book_keeping_where_no_vat_is_required'])
        # print(monthly_employee_report)


    def test_correctly_caclutates_book_keeping_in_monthly_employer_report_january(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #arrange + act
        test_set=[
            [ 6500 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_gross_payment_where_no_vat_is_required'] ],
            [ Decimal(138) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_employer_social_security_where_no_vat_is_required'] ],
            [ Decimal(5847.26) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_net_payment_where_no_vat_is_required'] ],
            [ Decimal(390) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_income_tax_where_no_vat_is_required'] ],
            [ Decimal(400.74) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_social_security_where_no_vat_is_required'] ],
            [ Decimal(2250) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['list_of_names_and_monthly_net_where_no_vat_is_required'][0]['monthly_net'] ],
            
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_book_keeping_in_monthly_employer_report_february(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=2)
        #arrange + act
        test_set=[
            [ 10500 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_gross_payment_where_no_vat_is_required'] ],
            [ Decimal(379.12) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_employer_social_security_where_no_vat_is_required'] ],
            [ Decimal(9414.52) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_net_payment_where_no_vat_is_required'] ],
            [ Decimal(600) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_income_tax_where_no_vat_is_required'] ],
            [ Decimal(864.6) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_social_security_where_no_vat_is_required'] ],
            [ Decimal(5152.26) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['list_of_names_and_monthly_net_where_no_vat_is_required'][0]['monthly_net'] ],
        ]
        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
    def test_correctly_caclutates_book_keeping_in_monthly_employer_report_march(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=3)
        #arrange + act
        test_set=[
            [ 13500 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_gross_payment_where_no_vat_is_required'] ],
            [ Decimal(327.75) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_employer_social_security_where_no_vat_is_required'] ],
            [ Decimal(11092.26) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_net_payment_where_no_vat_is_required'] ],
            [ Decimal(1655) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_income_tax_where_no_vat_is_required'] ],
            [ Decimal(1080.49) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['sum_of_social_security_where_no_vat_is_required'] ],
            [ Decimal(3325) * 1 , monthly_employer_report['book_keeping_where_no_vat_is_required']['list_of_names_and_monthly_net_where_no_vat_is_required'][0]['monthly_net'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])


    def test_monthly_employer_report_has_all_book_keeping_where_vat_is_required_fields(self):
        """ calculate book keeping where vat is required for employer monthly report """
        #arrange
        book_keeping_fields = [
            'list_of_names_and_income_tax_where_vat_is_required',
            'sum_of_income_tax_where_vat_is_required',
            'list_of_names_and_social_security_employer_where_vat_is_required',
            'sum_of_social_security_employer_where_vat_is_required',
            'sum_of_social_security_where_vat_is_required'
        ]
        #act
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #assert
        for field in book_keeping_fields:
            self.assertIn(field , monthly_employer_report['book_keeping_where_vat_is_required'])
        # print(monthly_employer_report['book_keeping_where_vat_is_required']['list_of_names_and_income_tax_where_vat_is_required'])


    def test_correctly_caclutates_book_keeping_where_vat_is_required_in_monthly_employer_report_january(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=1)
        #arrange + act
        test_set=[
            [ Decimal(0) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['list_of_names_and_income_tax_where_vat_is_required'][0]['income_tax'] ],
            [ Decimal(696.2) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['sum_of_income_tax_where_vat_is_required'] ],
            [ Decimal(837.74) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['sum_of_social_security_employer_where_vat_is_required'] ],
            [ Decimal(2812.74) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['sum_of_social_security_where_vat_is_required'] ],
            
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_book_keeping_where_vat_is_required_in_monthly_employer_report_february(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=2)
        #arrange + act
        test_set=[
            [ Decimal(354) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['list_of_names_and_income_tax_where_vat_is_required'][1]['income_tax'] ],
            [ Decimal(495.6) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['sum_of_income_tax_where_vat_is_required'] ],
            [ Decimal(534.37) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['sum_of_social_security_employer_where_vat_is_required'] ],
            [ Decimal(1909.37) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['sum_of_social_security_where_vat_is_required'] ],
        ]
        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
    def test_correctly_caclutates_book_keeping_where_vat_is_required_in_monthly_employer_report_march(self):
        #arrange
        monthly_employer_report = self.reports_maker.monthly_employer_report(for_year=2015, for_month=3)
        #arrange + act
        test_set=[
            [ Decimal(0) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['list_of_names_and_income_tax_where_vat_is_required'][0]['income_tax'] ],
            [ Decimal(212.4) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['sum_of_income_tax_where_vat_is_required'] ],
            # [ Decimal(172.5) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['list_of_names_and_social_security_employer_where_vat_is_required'][0]['social_security_employer'] ],
            [ Decimal(586.12) *1 , monthly_employer_report['book_keeping_where_vat_is_required']['sum_of_social_security_employer_where_vat_is_required'] ],
        ]

        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

	#quarterly_social_security_report suite
    def test_monthly_employee_report_has_all_fields(self):
        #arrange 
        fields = [
            'first_name',
            'last_name',
            'government_id',
            'birthday',
            'months_data',
        ]
        #act
        quarterly_social_security_report = self.reports_maker.quarterly_social_security_report(for_year=2015, for_month=1)
        #assert
        for field in fields:
            self.assertIn(field , quarterly_social_security_report[0])
        # print(monthly_employee_report)

    def test_correctly_caclutates_quarterly_social_security_report_january(self):
        quarterly_social_security_report = self.reports_maker.quarterly_social_security_report(for_year=2015, for_month=1)
        test_set=[
            # does not have to pay tax
            [ Decimal(175)*1 , quarterly_social_security_report[0]['months_data'][0]['social_security_employee'] ],

            [ Decimal(840)*1 , quarterly_social_security_report[1]['months_data'][0]['social_security_employee'] ],

            [ Decimal(0)*1 , quarterly_social_security_report[2]['months_data'][0]['social_security_employee'] ],

            [ Decimal(262.74)*1 , quarterly_social_security_report[3]['months_data'][0]['social_security_employee'] ],

            [ Decimal(960)*1 , quarterly_social_security_report[4]['months_data'][0]['social_security_employee'] ],

            [ Decimal(0)*1 , quarterly_social_security_report[5]['months_data'][0]['social_security_employee'] ],
        ]


        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_quarterly_social_security_report_february(self):
        quarterly_social_security_report = self.reports_maker.quarterly_social_security_report(for_year=2015, for_month=1)
        test_set=[
            # does not have to pay tax
            [ Decimal(175)*1 , quarterly_social_security_report[0]['months_data'][1]['social_security_employee'] ],

            [ Decimal(720)*1 , quarterly_social_security_report[1]['months_data'][1]['social_security_employee'] ],

            [ Decimal(247.74)*1 , quarterly_social_security_report[2]['months_data'][1]['social_security_employee'] ],

            [ Decimal(0)*1 , quarterly_social_security_report[3]['months_data'][1]['social_security_employee'] ],

            [ Decimal(480)*1 , quarterly_social_security_report[4]['months_data'][1]['social_security_employee'] ],

            [ Decimal(237.74)*1 , quarterly_social_security_report[5]['months_data'][1]['social_security_employee'] ],
        ]


        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])

    def test_correctly_caclutates_quarterly_social_security_report_march(self):
        quarterly_social_security_report = self.reports_maker.quarterly_social_security_report(for_year=2015, for_month=1)
        test_set=[
            # does not have to pay tax
            [ Decimal(175)*1 , quarterly_social_security_report[0]['months_data'][2]['social_security_employee'] ],

            [ Decimal(660)*1 , quarterly_social_security_report[1]['months_data'][2]['social_security_employee'] ],

            [ Decimal(0)*1 , quarterly_social_security_report[2]['months_data'][2]['social_security_employee'] ],

            [ Decimal(540)*1 , quarterly_social_security_report[3]['months_data'][2]['social_security_employee'] ],

            [ Decimal(720)*1 , quarterly_social_security_report[4]['months_data'][2]['social_security_employee'] ],

            [ Decimal(212.74)*1 , quarterly_social_security_report[5]['months_data'][2]['social_security_employee'] ],
        ]


        #assert
        for single_test in test_set:
            self.assertEqual(single_test[0] , single_test[1])
