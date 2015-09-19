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

    def calculate_social_security_employee_by_employee_monthly_entry(self, entry):
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
        return vat_percentage * sum_of_gross_payment_where_no_vat_is_required
    def calculate_vat_for_employee_for_month(self, employee, for_month , for_year):
        employee_data = self.getter.get_employee_data_by_month(employee=employee,  for_year=for_year, for_month=for_month)
        employer_data = self.getter.get_employer_data_by_month(employee=employee,  for_year=for_year, for_month=for_month)
        system_data = self.getter.get_system_data_by_month(for_year=for_year, for_month=for_month)
        if employee_data is None:
            return 0
        return calculate_output_tax(overall_gross=employee_data.gross_payment, vat_percentage=system_data.vat_percentage,is_required_to_pay_vat=employer_data.is_required_to_pay_vat )
        

    def internal_get_entries_for_month(self , for_year, for_month , is_required_to_pay_vat=True):
        employer_entries = Monthly_employer_data.objects.select_related('employee').filter(is_required_to_pay_vat=is_required_to_pay_vat, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month)
        for employer_entry in employer_entries:
            employer_entry.Monthly_employee_data_as_object = Monthly_employee_data.objects.get(employee=employer_entry.employee, is_approved=True, for_year=for_year, for_month=for_month)
            employer_entry.Monthly_employee_data = vars(employer_entry.Monthly_employee_data_as_object)
        return employer_entries


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
            if entry.is_required_to_pay_vat:
                sum_vat += entry.Monthly_employee_data['gross_payment'] * vat_percentage
            sum_gross += entry.Monthly_employee_data['gross_payment']
        return sum_vat + sum_gross

    def get_sum_of_income_tax(self , for_year, for_month):
        unparsed_employees_that_got_paid_this_month = self.internal_get_all_of_employees_that_got_paid_this_month(for_year=for_year, for_month=for_month)
        employees_that_got_paid_this_month = self.internal_join_all_of_employees_that_got_paid_this_month(unparsed_employees_that_got_paid_this_month)
        sum_to_return = 0
        # return employees_that_got_paid_this_month[1].employee.id
        # return self.internal_calculate_income_tax(entry=employees_that_got_paid_this_month[1])
        for entry in employees_that_got_paid_this_month:
            sum_to_return += self.internal_calculate_income_tax(employee=entry.employee , for_year=for_year , for_month=for_month)
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
        return self.internal_calculate_income_tax_recursion(employee=employee, for_year=for_year, for_month=for_month , **kwargs)['income_tax_for_this_month']

    # def internal_get_first_month_for_user(self, entry , for_month):
    #     try:
    #         first_entry_in_year = Monthly_employee_data.objects.filter(employee=entry.employee , for_year=entry.for_year , is_approved=True).order_by('-for_month')[0]
    #     except AttributeError as e:
    #         return for_month
    #     return first_entry_in_year.for_month

    def internal_calculate_income_tax_recursion(self , employee , for_year , for_month , **kwargs ):
        entry = self.getter.get_employee_data_by_month(employee=employee, for_year=for_year, for_month=for_month )
        no_tax_dict = False
        try:
            if entry.gross_payment is None:
                no_tax_dict = True
        except AttributeError:
            no_tax_dict = True
        
        if for_month == 1:
            accumulated_income_tax_not_including_this_month = 0
        else:
            accumulated_income_tax_not_including_this_month = self.internal_calculate_income_tax_recursion(employee , for_year , for_month -1 , **kwargs)['accumulated_income_tax_not_including_this_month']
            # print('-------------------- accumulated_income_tax_not_including_this_month: {0}\n'.format(accumulated_income_tax_not_including_this_month))
        if no_tax_dict:
            income_tax_for_this_month = 0
        else:
            system_data = self.getter.get_system_data_by_month(for_year=for_year , for_month=for_month)
            employer_data = self.getter.get_relevant_employer_data_for_empty_month(for_year=for_year, for_month=for_month, employee=employee)
            if employer_data is None:
                raise
        
            employee_data = vars(entry)
            vat_percentage = system_data.vat_percentage
            if employer_data.is_required_to_pay_vat:
                vat_due_this_month = employee_data['gross_payment'] * vat_percentage
            else:
                vat_due_this_month = 0
        
            accumulated_gross_including_this_month = self.internal_get_accumulated_gross_including_this_month(for_year=entry.for_year,for_month=for_month,employee_id=entry.employee_id)
            income_tax_for_this_month = calculate_income_tax(overall_gross=employee_data['gross_payment'],income_tax_threshold=employer_data.income_tax_threshold,lower_tax_threshold=employer_data.lower_tax_threshold,upper_tax_threshold=employer_data.upper_tax_threshold,is_required_to_pay_income_tax=employer_data.is_required_to_pay_income_tax,exact_income_tax_percentage=employer_data.exact_income_tax_percentage,accumulated_gross_including_this_month=accumulated_gross_including_this_month,accumulated_income_tax_not_including_this_month=accumulated_income_tax_not_including_this_month,vat_due_this_month=vat_due_this_month)
        return { 'accumulated_income_tax_not_including_this_month' : income_tax_for_this_month + accumulated_income_tax_not_including_this_month, 'income_tax_for_this_month' : income_tax_for_this_month } 

    def internal_get_accumulated_gross_including_this_month(self , for_year, for_month , employee_id):
        total = Monthly_employee_data.objects.filter(employee=employee_id , for_year=for_year , for_month__lte=for_month , is_approved=True).aggregate(my_total = Sum('gross_payment'))
        return total['my_total']

    
class cross_calculations(object):
    """docstring for cross_calculations"""
    def __init__(self, user_id):
        super(cross_calculations, self).__init__()
        self.user_id = user_id
        if Employer.is_employer(user_id):
            self.employer = Employer.get_employer_from_user(user_id)
        self.getter = data_getter()
        self.income_tax = income_tax_calculations(user_id=user_id)
        self.social_security = social_security_calculations(user_id=user_id)
        self.vat = vat_calculations(user_id=user_id)


    def monthly_employee_report(self, employee, for_year, for_month):
        monthly_employee_data = self.getter.get_employee_data_by_month(employee=employee,for_year=for_year,for_month=for_month)
        if monthly_employee_data is None:
            salary = 0
            general_expenses = 0
            social_security_employee_due_this_month = 0
            gross_payment = 0
        else:
            salary = monthly_employee_data.salary
            general_expenses = monthly_employee_data.general_expenses
            social_security_employee_due_this_month = self.social_security.calculate_social_security_employee_by_employee_monthly_entry(monthly_employee_data)['total']
            gross_payment = monthly_employee_data.gross_payment
        
        report_data = {
            'salary': salary,
            'general_expenses': general_expenses,
            'income_tax_due_this_month': self.income_tax.calculate_income_tax_for_single_employee_for_month(employee=employee, for_year=for_year, for_month=for_month),
            'social_security_employee_due_this_month': social_security_employee_due_this_month,
            'vat_due_this_month': self.vat.calculate_vat_for_employee_for_month(employee=employee, for_year=for_year, for_month=for_month),
        }
        report_data['monthly_net'] = calculate_monthly_net(overall_gross=gross_payment , output_tax=report_data['vat_due_this_month'] , social_security_employee=report_data['social_security_employee_due_this_month'] , income_tax=report_data['income_tax_due_this_month'])
        return report_data


    def get_sum_of_employer_social_security_where_no_vat_is_required(self, for_year , for_month):
        entries = self.vat.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=False)
        sum_to_return = 0
        return_arr = []
        for entry in entries:
            social_security_dict = self.social_security.internal_calculate_social_security_employer(entry.Monthly_employee_data_as_object)
            sum_to_return += social_security_dict['total']
        return sum_to_return

    def get_sum_of_net_payment_where_no_vat_is_required(self, for_year , for_month):
        sum_to_return = 0
        for row in self.get_list_of_names_and_monthly_net_where_no_vat_is_required(for_year=for_year , for_month=for_month):
            sum_to_return += row['monthly_net']
        return sum_to_return


    def get_list_of_names_and_monthly_net_where_no_vat_is_required(self, for_year , for_month):
        entries = self.vat.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=False)
        list_of_employees = []
        for entry in entries:
            monthly_employee_report = self.monthly_employee_report(employee=entry.employee, for_year=for_year , for_month=for_month)
            list_of_employees.append(
            	{ 'monthly_net' : monthly_employee_report['monthly_net'] , 'name' : '{0} {1}'.format(entry.employee.user.first_name ,entry.employee.user.last_name) })
        return list_of_employees

    def get_sum_of_income_tax_where_no_vat_is_required(self , for_year , for_month):
        entries = self.vat.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=False)
        sum_to_return = 0
        for entry in entries:
            sum_to_return += self.income_tax.calculate_income_tax_for_single_employee_for_month(employee=entry.employee, for_year=for_year , for_month=for_month)
        return sum_to_return

    def get_sum_of_social_security_where_no_vat_is_required(self, for_year , for_month):
        entries = self.vat.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=False)
        sum_to_return = 0
        return_arr = []
        for entry in entries:
            social_security_dict = self.social_security.calculate_social_security_employee_by_employee_monthly_entry(entry.Monthly_employee_data_as_object)
            sum_to_return += social_security_dict['total']
            social_security_dict = self.social_security.internal_calculate_social_security_employer(entry.Monthly_employee_data_as_object)
            sum_to_return += social_security_dict['total']        
        return sum_to_return    




class data_getter(object):
    """docstring for data_getter"""
    def __init__(self):
        super(data_getter, self).__init__()
    
    def get_system_data_by_month(self , for_year , for_month):
        # print('for_year: {0} , for_month: {1}'.format(for_year , for_month))
        return Monthly_system_data.objects.filter(for_month=for_month , for_year=for_year).latest('created')

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







