from .tests_imports import * 

class ModelsTestCase(TestCase):
    def __init__(self,*args, **kwargs):
        super(ModelsTestCase, self).__init__(*args,**kwargs)
        self.myGenerator = factories.MyGenerators()
    def setUp(self):
        pass
    # def test_orm(self): 
        # self.myGenerator.generateInitialControlledState()
        # first_employer = Employer.objects.order_by('-id')[0]
        # self.reports_maker = reports_maker.ReportsMaker(employer=first_employer)

        # employer = Employer.objects.order_by('-id')[0]
        # self.myGenerator = factories.MyGenerators()
        # self.data_getter = data_getter()
        # self.income_tax = income_tax_calculations(user_id=employer.user.id)
        # self.social_security = social_security_calculations(user_id=employer.user.id)
        # self.vat = vat_calculations(user_id=employer.user.id)
        # self.cross = cross_calculations(user_id=employer.user.id)

        
        # employee = Employee.objects.order_by('id')[1]
        # self.cross.monthly_employee_report_to_db(employee=employee, for_year=2015, for_month=1)
        # monthly_employee_report_to_db = Monthly_employee_report_data.objects.get(employee=employee,for_month=1, for_year=2015)
        # print(monthly_employee_report_to_db.monthly_employee_social_security_report_data.total)



    def test_insert_monthly_employee_data_with_cost_or_gross_set_to_gross_is_uninfluenced(self):
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)
        self.myGenerator.generate_monthly_system_data()

        #january
        factories.MonthlyEmployerDataFactory(
            employee=employee,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = True,
            is_required_to_pay_income_tax = False,
        )
        factories.MonthlyEmployeeDataFactory(
            employee=employee,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(5000),
            salary = Decimal(4500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = True,
            gross_payment_from_others = Decimal(1000)
        )

        #act
        monthly_employee_data = Monthly_employee_data.objects.all()[0]

        #assert
        self.assertIsInstance(monthly_employee_data.id , int)
        self.assertEqual(monthly_employee_data.employee.id , employee.id)
        self.assertEqual(monthly_employee_data.gross_payment , 5000)

    def test_insert_monthly_employee_data_with_cost_or_gross_set_to_cost_is_influenced_when_gross_is_lower_than_threshold(self):
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)
        self.myGenerator.generate_monthly_system_data()

        #january
        factories.MonthlyEmployerDataFactory(
            employee=employee,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = False,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = 0,
            upper_tax_threshold = Decimal(0.14),
            income_tax_threshold = Decimal(3000),
            exact_income_tax_percentage = 0,
            gross_or_cost = False
        )
        factories.MonthlyEmployeeDataFactory(
            employee=employee,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(4000),
            salary = Decimal(3500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = Decimal(3000)
        )

        #act
        monthly_employee_data = Monthly_employee_data.objects.all()[0]

        #assert
        self.assertIsInstance(monthly_employee_data.id , int)
        self.assertEqual(monthly_employee_data.employee.id , employee.id)
        self.assertEqual(monthly_employee_data.gross_payment , Decimal(3866.6) * 1 )

    def test_insert_monthly_employee_data_with_cost_or_gross_set_to_cost_is_influenced_when_gross_is_higher_than_threshold(self):
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)
        self.myGenerator.generate_monthly_system_data()

        #january
        factories.MonthlyEmployerDataFactory(
            employee=employee,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = True,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = 0,
            upper_tax_threshold = Decimal(0.14),
            income_tax_threshold = Decimal(3000),
            exact_income_tax_percentage = Decimal(0.03),
            gross_or_cost = False
        )
        factories.MonthlyEmployeeDataFactory(
            employee=employee,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(8000),
            salary = Decimal(7500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )

        #act
        monthly_employee_data = Monthly_employee_data.objects.all()[0]

        #assert
        self.assertIsInstance(monthly_employee_data.id , int)
        self.assertEqual(monthly_employee_data.employee.id , employee.id)
        self.assertEqual(monthly_employee_data.gross_payment , Decimal(7656.07) * 1 )


    def test_insert_monthly_employee_data_with_cost_or_gross_set_to_cost_generates_updated_results(self):
        employer = factories.EmployerFactory()
        employee = factories.EmployeeFactory(employer=employer)
        self.myGenerator.generate_monthly_system_data()
        self.reports_maker = reports_maker.ReportsMaker(employer=employer)

        #january
        factories.MonthlyEmployerDataFactory(
            employee=employee,
            for_year = 2015,
            for_month = 1,
            is_required_to_pay_vat = True,
            is_required_to_pay_income_tax = True,
            lower_tax_threshold = 0,
            upper_tax_threshold = Decimal(0.14),
            income_tax_threshold = Decimal(3000),
            exact_income_tax_percentage = Decimal(0.03),
            gross_or_cost = False
        )
        factories.MonthlyEmployeeDataFactory(
            employee=employee,
            for_year = 2015,
            for_month = 1,
            gross_payment = Decimal(8000),
            salary = Decimal(7500),
            general_expenses = Decimal(500),
            is_required_to_pay_social_security = True,
            is_employer_the_main_employer = False,
            gross_payment_from_others = 0
        )

        populate_db_with_the_results_of_calculations_for_all_months() 

        #act
        monthly_employee_data = Monthly_employee_data.objects.all()[0]
        monthly_employee_report = self.reports_maker.monthly_employee_report(employee=employee , for_year=2015 , for_month=1)
        # print(monthly_employee_report)
        
        #assert
        self.assertIsInstance(monthly_employee_data.id , int)
        self.assertEqual(monthly_employee_data.employee.id , employee.id)
        self.assertEqual(monthly_employee_data.gross_payment , Decimal(7656.07) * 1 )
        self.assertEqual(monthly_employee_report['monthly_net'] , Decimal(7844.4) * 1 )

    # def test_create_custom_filter(self):
    #     self.myGenerator.generateInitialControlledState()
    #     factories.MonthlyEmployeeDataFactory(for_year=1999)
    #     for_year = 2015
    #     for_month = 1
    #     coco = (for_year * 12) + for_month
    #     ordered_list = Monthly_employee_data.objects.raw('SELECT * FROM reports_monthly_employee_data WHERE (for_year * 12) + for_month <= {0} ORDER BY (for_year * 12) + for_month DESC '.format(coco))
    #     print(ordered_list[0].id)

    #     for single in ordered_list:
    #         print(single.id)
    #         print('year , month {0} , {1}'.format(single.for_year , single.for_month))

    def test_can_add_a_monthly_employee_report_data_object_to_db(self):
        #arrange
        employee = factories.EmployeeFactory()
        monthly_employee_report_data = Monthly_employee_report_data(
            employee = employee ,
            entered_by = 'admin',
            for_month = 1 ,
            for_year = 2015 ,
            income_tax = 100.5 ,
            vat = 565.55 ,
            input_tax_vat = 300,
            net = 5
        )
        #act
        monthly_employee_report_data.save()

        #assert
        self.assertTrue(Monthly_employee_report_data.objects.get(id=monthly_employee_report_data.id))
