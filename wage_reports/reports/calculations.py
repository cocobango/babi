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
        system_data = self.getter.get_system_data_by_month(for_year=for_year , for_month=for_month)
        sum_to_return = 0
        entries = Monthly_employee_data.objects.select_related('employee').filter(is_required_to_pay_social_security=True, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month)
        for entry in entries:
            # return entry.id
            response = calculate_social_security_employee(overall_gross=entry.gross_payment,social_security_threshold=system_data.social_security_threshold,lower_employee_social_security_percentage=system_data.lower_employee_social_security_percentage,upper_employee_social_security_percentage=system_data.upper_employee_social_security_percentage,is_required_to_pay_social_security=entry.is_required_to_pay_social_security, is_employer_the_main_employer=entry.is_employer_the_main_employer, gross_payment_from_others=entry.gross_payment_from_others)
            sum_to_return += response['sum_to_calculate_as_lower_social_security_percentage']
        return sum_to_return

class settings_data_getter(object):
    """docstring for settings_data_getter"""
    def __init__(self):
        super(settings_data_getter, self).__init__()
    
    def get_system_data_by_month(self , for_year , for_month):
    	return Monthly_system_data.objects.filter(for_month=for_month , for_year=for_year).latest('created')