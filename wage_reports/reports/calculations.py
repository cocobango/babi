from decimal import *

from django.db.models import Count, Min, Sum, Avg
from .models import Monthly_employer_data, Monthly_employee_data, Monthly_system_data, Employee , Employer , Locked_months

from .helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_social_security_employer , calculate_social_security_employee , calculate_income_tax , calculate_output_tax , calculate_monthly_net

class social_security_calculations(object):
    """docstring for social_security_calculations"""
    def __init__(self, user_id):
        super(social_security_calculations, self).__init__()
        self.user_id = user_id
        if Employer.is_employer(user_id):
            self.employer = Employer.get_employer_from_user(user_id)
        self.getter = settings_data_getter()
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
            response_employee = self.internal_calculate_social_security_employee(entry)
            response_employer = self.internal_calculate_social_security_employer(entry)
            sum_to_return += response_employee['total'] + response_employer['total']
        return sum_to_return


    def get_count_of_employees_that_do_not_exceed_the_social_security_threshold_by_employer(self , for_year, for_month):
        entries = self.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_social_security=True)
        count = 0
        for entry in entries:
            response_employee = self.internal_calculate_social_security_employee(entry)
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
                response = self.internal_calculate_social_security_employee(entry)
            else:
                response = self.internal_calculate_social_security_employer(entry)
            if upper_or_lower == 'upper':
                sum_to_return += response['sum_to_calculate_as_upper_social_security_percentage']
            else:
                sum_to_return += response['sum_to_calculate_as_lower_social_security_percentage']
        return sum_to_return
    
    def internal_get_entries_for_month(self , for_year, for_month , is_required_to_pay_social_security=True):
        return Monthly_employee_data.objects.select_related('employee').filter(is_required_to_pay_social_security=is_required_to_pay_social_security, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month)

    def internal_calculate_social_security_employee(self, entry):
        system_data = self.getter.get_system_data_by_month(for_year=entry.for_year , for_month=entry.for_month)
        return calculate_social_security_employee(overall_gross=entry.gross_payment,social_security_threshold=system_data.social_security_threshold,lower_employee_social_security_percentage=system_data.lower_employee_social_security_percentage,upper_employee_social_security_percentage=system_data.upper_employee_social_security_percentage,is_required_to_pay_social_security=entry.is_required_to_pay_social_security, is_employer_the_main_employer=entry.is_employer_the_main_employer, gross_payment_from_others=entry.gross_payment_from_others)

    def internal_calculate_social_security_employer(self, entry):
        system_data = self.getter.get_system_data_by_month(for_year=entry.for_year , for_month=entry.for_month)
        return calculate_social_security_employer(overall_gross=entry.gross_payment,social_security_threshold=system_data.social_security_threshold,lower_employer_social_security_percentage=system_data.lower_employer_social_security_percentage,upper_employer_social_security_percentage=system_data.upper_employer_social_security_percentage,is_required_to_pay_social_security=entry.is_required_to_pay_social_security)

class vat_calculations(object):
    """docstring for vat_calculations"""
    def __init__(self, user_id):
        super(vat_calculations, self).__init__()
        self.user_id = user_id
        if Employer.is_employer(user_id):
            self.employer = Employer.get_employer_from_user(user_id)
        self.getter = settings_data_getter()

    def get_sum_of_gross_payment_where_no_vat_is_required(self , for_year, for_month):
        entries = self.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=False)
        sum_to_return = 0
        return_arr = []
        for entry in entries:
            # return_arr.append(vars(entry.Monthly_employee_data)['gross_payment']) 
            sum_to_return += entry.Monthly_employee_data['gross_payment']
        return sum_to_return

    def internal_get_entries_for_month(self , for_year, for_month , is_required_to_pay_vat=True):
        employer_entries = Monthly_employer_data.objects.select_related('employee').filter(is_required_to_pay_vat=is_required_to_pay_vat, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month)
        for employer_entry in employer_entries:
            employer_entry.Monthly_employee_data = vars(Monthly_employee_data.objects.get(employee=employer_entry.employee, is_approved=True, for_year=for_year, for_month=for_month))
        return employer_entries









class settings_data_getter(object):
    """docstring for settings_data_getter"""
    def __init__(self):
        super(settings_data_getter, self).__init__()
    
    def get_system_data_by_month(self , for_year , for_month):
        return Monthly_system_data.objects.filter(for_month=for_month , for_year=for_year).latest('created')