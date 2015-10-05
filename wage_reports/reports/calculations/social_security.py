from django.db.models import Count, Min, Sum, Avg
from ..models import Monthly_employer_data, Monthly_employee_data, Monthly_system_data, Employee , Employer , Locked_months , Monthly_employee_report_data , Monthly_employee_social_security_report_data

from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_social_security_employer , calculate_social_security_employee , calculate_income_tax , calculate_output_tax , calculate_monthly_net

from .data_getter import data_getter


class social_security_calculations(object):
    """docstring for social_security_calculations"""
    def __init__(self, user_id):
        super(social_security_calculations, self).__init__()
        self.user_id = user_id
        if Employer.is_employer(user_id):
            self.employer = Employer.get_employer_from_user(user_id)
        self.getter = data_getter()
    #employer
    def get_count_of_employees_that_are_required_to_pay_social_security_by_employer(self , for_year, for_month):
        return Monthly_employee_data.objects.select_related('employee').filter(is_required_to_pay_social_security=True, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month).count()

    def get_sum_of_gross_payment_of_employees_that_are_required_to_pay_social_security_by_employer(self , for_year, for_month):
        return Monthly_employee_data.objects.select_related('employee').filter(is_required_to_pay_social_security=True, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month).aggregate(my_total = Sum('gross_payment'))
    def get_sum_of_lower_employee_social_security_by_employer(self , for_year, for_month):
        return self.get_sum_of_social_security_of_type_by_employer(for_year = for_year, for_month = for_month , employee_or_employer = 'employee' , upper_or_lower = 'lower')

    def get_sum_of_upper_employee_social_security_by_employer(self , for_year, for_month):
        return self.get_sum_of_social_security_of_type_by_employer(for_year = for_year, for_month = for_month , employee_or_employer = 'employee' , upper_or_lower = 'upper')

    def get_sum_of_lower_employer_social_security_by_employer(self , for_year, for_month):
        return self.get_sum_of_social_security_of_type_by_employer(for_year = for_year, for_month = for_month , employee_or_employer = 'employer' , upper_or_lower = 'lower')

    def get_sum_of_upper_employer_social_security_by_employer(self , for_year, for_month):
        return self.get_sum_of_social_security_of_type_by_employer(for_year = for_year, for_month = for_month , employee_or_employer = 'employer' , upper_or_lower = 'upper')

    def get_total_of_social_security_due_by_employer(self , for_year, for_month):
        entries = self.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_social_security=True)
        sum_to_return = 0
        for entry in entries:
            response_employee = self.calculate_social_security_employee_by_employee_monthly_entry(entry)
            response_employer = self.internal_calculate_social_security_employer(entry)
            sum_to_return += response_employee['total'] + response_employer['total']
        return sum_to_return


    def get_count_of_employees_that_do_not_exceed_the_social_security_threshold_by_employer(self , for_year, for_month):
        entries = self.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_social_security=True)
        count = 0
        for entry in entries:
            response_employee = self.calculate_social_security_employee_by_employee_monthly_entry(entry)
            if response_employee['standard_sum'] == 0 and response_employee['diminished_sum'] > 0:
                count +=1
        return count

    # internal
    def get_sum_of_social_security_of_type_by_employer(self , for_year, for_month , employee_or_employer , upper_or_lower):
        sum_to_return = 0
        entries = self.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_social_security=True)
        for entry in entries:
            # return entry.id
            if employee_or_employer == 'employee':
                response = self.calculate_social_security_employee_by_employee_monthly_entry(entry)
            else:
                response = self.internal_calculate_social_security_employer(entry)
            if upper_or_lower == 'upper':
                sum_to_return += response['sum_to_calculate_as_upper_social_security_percentage']
            else:
                sum_to_return += response['sum_to_calculate_as_lower_social_security_percentage']
        return sum_to_return
    
    def internal_get_entries_for_month(self , for_year, for_month , is_required_to_pay_social_security=True):
        return Monthly_employee_data.objects.select_related('employee').filter(is_required_to_pay_social_security=is_required_to_pay_social_security, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month)
    def internal_get_all_employees(self):
        return Employee.objects.filter(employer = self.employer)

    def calculate_social_security_employee_by_employee_monthly_entry(self, entry):
        if entry is None:
            return { 'sum_to_calculate_as_lower_social_security_percentage' : 0 , 'sum_to_calculate_as_upper_social_security_percentage' : 0 ,'diminished_sum' : 0 , 'standard_sum' : 0 , 'total' : 0}
        system_data = self.getter.get_system_data_by_month(for_year=entry.for_year , for_month=entry.for_month)
        return calculate_social_security_employee(overall_gross=entry.gross_payment,social_security_threshold=system_data.social_security_threshold,lower_employee_social_security_percentage=system_data.lower_employee_social_security_percentage,upper_employee_social_security_percentage=system_data.upper_employee_social_security_percentage,is_required_to_pay_social_security=entry.is_required_to_pay_social_security, is_employer_the_main_employer=entry.is_employer_the_main_employer, gross_payment_from_others=entry.gross_payment_from_others)

    def internal_calculate_social_security_employer(self, entry):
        system_data = self.getter.get_system_data_by_month(for_year=entry.for_year , for_month=entry.for_month)
        return calculate_social_security_employer(overall_gross=entry.gross_payment,social_security_threshold=system_data.social_security_threshold,lower_employer_social_security_percentage=system_data.lower_employer_social_security_percentage,upper_employer_social_security_percentage=system_data.upper_employer_social_security_percentage,is_required_to_pay_social_security=entry.is_required_to_pay_social_security)


    def generate_quarterly_social_security_report(self, for_year, for_month):
        # get all employees
        all_employees = self.internal_get_all_employees()

        # for each employee get social security data for each of the 3 month in the quarter
        employees_months_data_that_includes_empty_entries = []
        for employee in all_employees:
            employees_months_data_that_includes_empty_entries.append(self.internal_get_social_security_data_for_quarter_that_starts_with_month( employee=employee , for_year=for_year , for_month=for_month))

        return_arr = []
        # for each none empty employee get append to return arr as months data
        for employee_data in employees_months_data_that_includes_empty_entries:
            include_in_report = False
            for x in range(0 , 3):
                if employee_data['months_data'][x]['social_security_employee'] != 0:
                    include_in_report = True
            if include_in_report:
                return_arr.append(employee_data)


        # for each employee add personal general data
        for entry in return_arr:
            employee = Employee.objects.select_related('user').get(id=entry['employee_id'])
            entry['first_name'] = employee.user.first_name
            entry['last_name'] = employee.user.last_name
            entry['government_id'] = employee.government_id
            entry['birthday'] = employee.birthday

        return return_arr


    def internal_get_social_security_data_for_quarter_that_starts_with_month(self, employee , for_year, for_month):
        months_data = []
        for x in range(0 , 3):
            months_data.append(self.internal_generate_quarterly_social_security_report_single_month(employee=employee , for_year=for_year , for_month=for_month + x) )
        return {
            'months_data': months_data ,
            'employee_id': employee.id
        }
        
    def internal_generate_quarterly_social_security_report_single_month(self, employee , for_year, for_month):
        monthly_employee_data = self.getter.get_employee_data_by_month(employee=employee,  for_year=for_year, for_month=for_month)
        if monthly_employee_data is None:
            return {
                'social_security_employee': 0,
                'gross_payment': 0
            }
        return {
            'social_security_employee': self.calculate_social_security_employee_by_employee_monthly_entry(monthly_employee_data)['total'],
            'gross_payment': monthly_employee_data.gross_payment 
        }
