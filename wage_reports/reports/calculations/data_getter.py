from django.db.models import Count, Min, Sum, Avg
from ..models import Monthly_employer_data, Monthly_employee_data, Monthly_system_data, Employee , Employer , Locked_months , Monthly_employee_report_data , Monthly_employee_social_security_report_data

from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_social_security_employer , calculate_social_security_employee , calculate_income_tax , calculate_output_tax , calculate_monthly_net


class data_getter(object):
    """docstring for data_getter"""
    def __init__(self):
        super(data_getter, self).__init__()
    
    def get_system_data_by_month(self , for_year , for_month):
        # print('for_year: {0} , for_month: {1}'.format(for_year , for_month))
        month_count_from_zero = (for_year * 12) + for_month
        try:
            return Monthly_system_data.objects.raw('SELECT * FROM reports_monthly_system_data WHERE (for_year * 12) + for_month <= {0} ORDER BY (for_year * 12) + for_month DESC '.format(month_count_from_zero))[0]
        except IndexError:
            raise                
        

    def get_employee_data_by_month(self , for_year , for_month , employee ):
        try:
            return Monthly_employee_data.objects.get(for_month=for_month , for_year=for_year , employee=employee , is_approved=True)
        except Exception as e:
            # print('cannot find data for employee: {0} in month: {1} and year {2}'.format(employee , for_month , for_year))
            return None

    def get_employer_data_by_month(self , for_year , for_month , employee):
        try:
            return Monthly_employer_data.objects.get(for_month=for_month , for_year=for_year , employee=employee , is_approved=True)
        except Exception as e:
            return None
    def get_employee_report_data_by_month(self , for_year , for_month , employee):
        try:
            return Monthly_employee_report_data.objects.get(employee=employee, for_year=for_year, for_month=for_month)
        except Exception as e:
            return None
    
    def get_employee_social_security_report_data_by_month(self , for_year , for_month , employee):
        try:
            return Monthly_employee_social_security_report_data.objects.get(employee=employee, for_year=for_year, for_month=for_month)
        except Exception as e:
            return None

    def get_relevant_employer_data_for_empty_month(self, for_year, for_month, employee):    
        try:
            return Monthly_employer_data.objects.filter(for_month__lte=for_month , for_year=for_year , employee=employee , is_approved=True).order_by('-for_month')[0]
        except IndexError:
            try:
                return Monthly_employer_data.objects.filter( for_year=for_year-1 , employee=employee , is_approved=True).order_by('-for_month')[0]
            except IndexError:
                return None
    def get_relevant_employee_data_for_empty_month(self, for_year, for_month, employee):    
        pass







