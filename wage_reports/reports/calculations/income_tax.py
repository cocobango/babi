from django.db.models import Count, Min, Sum, Avg
from ..models import Monthly_employer_data, Monthly_employee_data, Monthly_system_data, Employee , Employer , Locked_months , Monthly_employee_report_data , Monthly_employee_social_security_report_data

from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_social_security_employer , calculate_social_security_employee , calculate_income_tax , calculate_output_tax , calculate_monthly_net

from .data_getter import data_getter

class income_tax_calculations(object):
    """docstring for income_tax_calculations"""
    def __init__(self, user_id):
        super(income_tax_calculations, self).__init__()
        self.user_id = user_id
        if Employer.is_employer(user_id):
            self.employer = Employer.get_employer_from_user(user_id)
        self.getter = data_getter()

    def get_count_of_employees_that_got_paid_this_month(self , for_year, for_month):
        employees_that_got_paid_this_month = self.internal_get_all_of_employees_that_got_paid_this_month(for_year=for_year, for_month=for_month)
        return len(employees_that_got_paid_this_month['employees_that_are_required_to_pay_income_tax']) + len(employees_that_got_paid_this_month['employees_that_are_not_required_to_pay_income_tax'])
    
    def get_sum_of_gross_payment_and_vat_for_employees_that_got_paid_this_month(self , for_year, for_month):
        unparsed_employees_that_got_paid_this_month = self.internal_get_all_of_employees_that_got_paid_this_month(for_year=for_year, for_month=for_month)
        employees_that_got_paid_this_month = self.internal_join_all_of_employees_that_got_paid_this_month(unparsed_employees_that_got_paid_this_month)
        sum_vat = 0
        sum_gross = 0
        vat_percentage = self.getter.get_system_data_by_month(for_year=for_year , for_month=for_month).vat_percentage
        for entry in employees_that_got_paid_this_month:
            monthly_employee_report_data = self.getter.get_employee_report_data_by_month(employee=entry.employee, for_year=for_year, for_month=for_month)
            
            sum_vat += monthly_employee_report_data.vat 
            sum_gross += entry.Monthly_employee_data['gross_payment']
        return sum_vat + sum_gross

    def get_sum_of_income_tax(self , for_year, for_month):
        unparsed_employees_that_got_paid_this_month = self.internal_get_all_of_employees_that_got_paid_this_month(for_year=for_year, for_month=for_month)
        employees_that_got_paid_this_month = self.internal_join_all_of_employees_that_got_paid_this_month(unparsed_employees_that_got_paid_this_month)
        sum_to_return = 0
        for entry in employees_that_got_paid_this_month:
            monthly_employee_report_data = self.getter.get_employee_report_data_by_month(employee=entry.employee, for_year=for_year, for_month=for_month)
            sum_to_return += monthly_employee_report_data.income_tax
        return sum_to_return
   
    def internal_get_entries_for_month(self , for_year, for_month , is_required_to_pay_income_tax=True):
        employer_entries = Monthly_employer_data.objects.select_related('employee').filter(is_required_to_pay_income_tax=is_required_to_pay_income_tax, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month)
        for employer_entry in employer_entries:
            employer_entry.Monthly_employee_data = vars(Monthly_employee_data.objects.get(employee=employer_entry.employee, is_approved=True, for_year=for_year, for_month=for_month))
        return employer_entries

    def internal_get_all_of_employees_that_got_paid_this_month(self , for_year, for_month):
        employees_that_are_required_to_pay_income_tax = self.internal_get_entries_for_month(for_year=for_year, for_month=for_month , is_required_to_pay_income_tax=True)
        employees_that_are_not_required_to_pay_income_tax = self.internal_get_entries_for_month(for_year=for_year, for_month=for_month , is_required_to_pay_income_tax=False)
        return { 'employees_that_are_required_to_pay_income_tax' : employees_that_are_required_to_pay_income_tax , 'employees_that_are_not_required_to_pay_income_tax' : employees_that_are_not_required_to_pay_income_tax }

    def internal_join_all_of_employees_that_got_paid_this_month(self , employees_that_got_paid_this_month):
        employees_that_are_required_to_pay_income_tax = list(employees_that_got_paid_this_month['employees_that_are_required_to_pay_income_tax'])
        employees_that_are_not_required_to_pay_income_tax = list(employees_that_got_paid_this_month['employees_that_are_not_required_to_pay_income_tax'])
        employees_that_are_required_to_pay_income_tax.extend(employees_that_are_not_required_to_pay_income_tax)
        return employees_that_are_required_to_pay_income_tax

    def calculate_income_tax_for_single_employee_for_month(self, employee, for_month , for_year):
        return self.internal_calculate_income_tax(employee=employee ,for_year=for_year , for_month=for_month )
    def internal_calculate_income_tax(self , employee , for_year , for_month , **kwargs ):
        return self.internal_calculate_income_tax_recursion(employee=employee, for_year=for_year, for_month=for_month , **kwargs)

    # def internal_get_first_month_for_user(self, entry , for_month):
    #     try:
    #         first_entry_in_year = Monthly_employee_data.objects.filter(employee=entry.employee , for_year=entry.for_year , is_approved=True).order_by('-for_month')[0]
    #     except AttributeError as e:
    #         return for_month
    #     return first_entry_in_year.for_month
    def get_accumulated_sum_of_income_tax_until_month_for_user(self, employee, for_year, for_month):
        
        return Monthly_employee_report_data.objects.filter(employee=employee, for_year=for_year, for_month__lt=for_month).aggregate(my_total = Sum('income_tax'))['my_total'] or 0
    def internal_calculate_income_tax_recursion(self , employee , for_year , for_month , **kwargs ):
        entry = self.getter.get_employee_data_by_month(employee=employee, for_year=for_year, for_month=for_month )
        is_there_tax_due_for_this_month = True
        try:
            if entry.gross_payment is None:
                is_there_tax_due_for_this_month = False
        except AttributeError:
            is_there_tax_due_for_this_month = False
        
        accumulated_income_tax_not_including_this_month = self.get_accumulated_sum_of_income_tax_until_month_for_user(employee=employee, for_year=for_year, for_month=for_month)
        
            # print('-------------------- accumulated_income_tax_not_including_this_month: {0}\n'.format(accumulated_income_tax_not_including_this_month))
        if is_there_tax_due_for_this_month:
            system_data = self.getter.get_system_data_by_month(for_year=for_year , for_month=for_month)
            employer_data = self.getter.get_relevant_employer_data_for_empty_month(for_year=for_year, for_month=for_month, employee=employee)
            if employer_data is None:
                raise
        
            employee_data = vars(entry)
            vat_due_this_month = calculate_output_tax(overall_gross=employee_data['gross_payment'],vat_percentage=system_data.vat_percentage,is_required_to_pay_vat=employer_data.is_required_to_pay_vat)
        
            accumulated_gross_including_this_month = self.internal_get_accumulated_gross_including_this_month(for_year=entry.for_year,for_month=for_month,employee_id=entry.employee_id)
            income_tax_for_this_month = calculate_income_tax(overall_gross=employee_data['gross_payment'],income_tax_threshold=employer_data.income_tax_threshold,lower_tax_threshold=employer_data.lower_tax_threshold,upper_tax_threshold=employer_data.upper_tax_threshold,is_required_to_pay_income_tax=employer_data.is_required_to_pay_income_tax,exact_income_tax_percentage=employer_data.exact_income_tax_percentage,accumulated_gross_including_this_month=accumulated_gross_including_this_month,accumulated_income_tax_not_including_this_month=accumulated_income_tax_not_including_this_month,vat_due_this_month=vat_due_this_month)
            return income_tax_for_this_month
        return 0 

    def internal_get_accumulated_gross_including_this_month(self , for_year, for_month , employee_id):
        total = Monthly_employee_data.objects.filter(employee=employee_id , for_year=for_year , for_month__lte=for_month , is_approved=True).aggregate(my_total = Sum('gross_payment'))
        return total['my_total']
