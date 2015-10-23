from django.db.models import Count, Min, Sum, Avg
from ..models import Monthly_employer_data, Monthly_employee_data, Monthly_system_data, Employee , Employer , Locked_months , Monthly_employee_report_data , Monthly_employee_social_security_report_data

from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_social_security_employer , calculate_social_security_employee , calculate_income_tax , calculate_output_tax, calculate_input_tax , calculate_monthly_net

from .data_getter import data_getter

class vat_calculations(object):
    """docstring for vat_calculations"""
    def __init__(self, user_id):
        super(vat_calculations, self).__init__()
        self.user_id = user_id
        if Employer.is_employer(user_id):
            self.employer = Employer.get_employer_from_user(user_id)
        self.getter = data_getter()

    def get_sum_of_gross_payment_where_no_vat_is_required(self , for_year, for_month):
        entries = self.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=False)
        sum_to_return = 0
        return_arr = []
        for entry in entries:
            # return_arr.append(vars(entry.Monthly_employee_data)['gross_payment']) 
            sum_to_return += entry.Monthly_employee_data['gross_payment']
        return sum_to_return

    def get_count_of_employees_where_no_vat_is_required(self , for_year, for_month):
        entries = self.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=False)
        count = len(entries)
        return count

    def get_sum_of_vat_due_where_no_vat_is_required(self , for_year, for_month):
        sum_of_gross_payment_where_no_vat_is_required = self.get_sum_of_gross_payment_where_no_vat_is_required(for_year=for_year , for_month=for_month)
        vat_percentage = self.getter.get_system_data_by_month(for_year=for_year , for_month=for_month).vat_percentage
        return calculate_output_tax(overall_gross=sum_of_gross_payment_where_no_vat_is_required,vat_percentage=vat_percentage,is_required_to_pay_vat=True)
    
    def calculate_vat_for_employee_for_month(self, employee, for_month , for_year):
        employee_data = self.getter.get_employee_data_by_month(employee=employee,  for_year=for_year, for_month=for_month)
        employer_data = self.getter.get_employer_data_by_month(employee=employee,  for_year=for_year, for_month=for_month)
        system_data = self.getter.get_system_data_by_month(for_year=for_year, for_month=for_month)
        if employee_data is None:
            return [0, 0]
        output_tax = calculate_output_tax(overall_gross=employee_data.gross_payment, vat_percentage=system_data.vat_percentage,is_required_to_pay_vat=employer_data.is_required_to_pay_vat )
        input_tax = calculate_input_tax(overall_gross=employee_data.gross_payment, vat_percentage=system_data.vat_percentage,is_required_to_pay_vat=employer_data.is_required_to_pay_vat, is_npo=self.employer.is_npo )
        return [output_tax, input_tax]
        

    def internal_get_entries_for_month(self , for_year, for_month , is_required_to_pay_vat=True):
        employer_entries = Monthly_employer_data.objects.select_related('employee').filter(is_required_to_pay_vat=is_required_to_pay_vat, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month)
        for employer_entry in employer_entries:
            employer_entry.Monthly_employee_data_as_object = Monthly_employee_data.objects.get(employee=employer_entry.employee, is_approved=True, for_year=for_year, for_month=for_month)
            employer_entry.Monthly_employee_data = vars(employer_entry.Monthly_employee_data_as_object)
        return employer_entries
