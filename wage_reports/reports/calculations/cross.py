from django.db.models import Count, Min, Sum, Avg
from ..models import Monthly_employer_data, Monthly_employee_data, Monthly_system_data, Employee , Employer , Locked_months , Monthly_employee_report_data , Monthly_employee_social_security_report_data

from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_social_security_employer , calculate_social_security_employee , calculate_income_tax , calculate_output_tax , calculate_monthly_net

from .data_getter import data_getter
from .income_tax import income_tax_calculations
from .social_security import social_security_calculations
from .vat import vat_calculations
    
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
        monthly_employee_report_data = self.getter.get_employee_report_data_by_month(employee=employee, for_year=for_year, for_month=for_month)
        if monthly_employee_data is None or monthly_employee_report_data is None: 
            report_data = {
                'salary': 0,
                'general_expenses': 0,
                'income_tax_due_this_month': 0,
                'social_security_employee_due_this_month': 0,
                'vat_due_this_month': 0,
                'monthly_net': 0,
            }
            return report_data


        report_data = {
            'salary': monthly_employee_data.salary,
            'general_expenses': monthly_employee_data.general_expenses,
            'income_tax_due_this_month': monthly_employee_report_data.income_tax,
            'social_security_employee_due_this_month': monthly_employee_report_data.monthly_employee_social_security_report_data.total,
            'vat_due_this_month': monthly_employee_report_data.vat,
            'monthly_net': monthly_employee_report_data.net,
        }   
        return report_data
        

    def monthly_employee_report_to_db(self, employee, for_year, for_month):
        monthly_employee_data = self.getter.get_employee_data_by_month(employee=employee,for_year=for_year,for_month=for_month)
        if monthly_employee_data is None:
            gross_payment = 0
        else:
            gross_payment = monthly_employee_data.gross_payment
        social_security_response_dict = self.social_security.calculate_social_security_employee_by_employee_monthly_entry(monthly_employee_data)
        report_data = {
            'income_tax_due_this_month': self.income_tax.calculate_income_tax_for_single_employee_for_month(employee=employee, for_year=for_year, for_month=for_month),
            'social_security_employee_due_this_month': social_security_response_dict['total'],
            'vat_due_this_month': self.vat.calculate_vat_for_employee_for_month(employee=employee, for_year=for_year, for_month=for_month),
        }
        report_data['monthly_net'] = calculate_monthly_net(overall_gross=gross_payment , output_tax=report_data['vat_due_this_month'] , social_security_employee=report_data['social_security_employee_due_this_month'] , income_tax=report_data['income_tax_due_this_month'])

        monthly_employee_report_data = Monthly_employee_report_data(
            employee = employee ,
            entered_by = 'automatic',
            for_year = for_year ,
            for_month = for_month ,
            income_tax = report_data['income_tax_due_this_month'] ,
            vat = report_data['vat_due_this_month'] ,
            input_tax_vat = 0,
            net = report_data['monthly_net']
        )#FIXME: input tax vat needs to be calculated not stubbed as 0
        monthly_employee_report_data.save()
        monthly_employee_social_security_report_data = Monthly_employee_social_security_report_data(
            monthly_employee_report_data = monthly_employee_report_data,
            sum_to_calculate_as_lower_social_security_percentage = social_security_response_dict['sum_to_calculate_as_lower_social_security_percentage'],
            sum_to_calculate_as_upper_social_security_percentage = social_security_response_dict['sum_to_calculate_as_upper_social_security_percentage'],
            diminished_sum = social_security_response_dict['diminished_sum'],
            standard_sum = social_security_response_dict['standard_sum'],
            total = social_security_response_dict['total']
        )
        monthly_employee_social_security_report_data.save()
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
        return self.internal_get_sum_of_social_security_by_is_vat_required(for_year=for_year , for_month=for_month , is_required_to_pay_vat=False)
   
    def get_sum_of_social_security_where_vat_is_required(self, for_year , for_month):
        return self.internal_get_sum_of_social_security_by_is_vat_required(for_year=for_year , for_month=for_month , is_required_to_pay_vat=True)
   
    def internal_get_sum_of_social_security_by_is_vat_required(self, for_year , for_month , is_required_to_pay_vat):
        entries = self.vat.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=is_required_to_pay_vat)
        sum_to_return = 0
        for entry in entries:
            social_security_dict = self.social_security.calculate_social_security_employee_by_employee_monthly_entry(entry.Monthly_employee_data_as_object)
            sum_to_return += social_security_dict['total']
            social_security_dict = self.social_security.internal_calculate_social_security_employer(entry.Monthly_employee_data_as_object)
            sum_to_return += social_security_dict['total']        
        return sum_to_return    

    def get_list_of_names_and_income_tax_where_vat_is_required(self, for_year , for_month):
        entries = self.vat.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=True)
        list_of_employees = []
        for entry in entries:
            income_tax = self.income_tax.calculate_income_tax_for_single_employee_for_month(employee=entry.employee, for_year=for_year , for_month=for_month)
            list_of_employees.append(
                { 'income_tax' : income_tax , 'name' : '{0} {1}'.format(entry.employee.user.first_name ,entry.employee.user.last_name) })
        return list_of_employees

    def get_sum_of_income_tax_where_vat_is_required(self, for_year , for_month):
        sum_to_return = 0
        for row in self.get_list_of_names_and_income_tax_where_vat_is_required( for_year=for_year , for_month=for_month):
            sum_to_return += row['income_tax']
        return sum_to_return

    def get_list_of_names_and_social_security_employer_where_vat_is_required(self, for_year , for_month):
        entries = self.vat.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=True)
        list_of_employees = []
        for entry in entries:
            social_security_dict = self.social_security.internal_calculate_social_security_employer(entry.Monthly_employee_data_as_object)
            list_of_employees.append(
                { 'social_security_employer' : social_security_dict['total'] , 'name' : '{0} {1}'.format(entry.employee.user.first_name ,entry.employee.user.last_name) })
        return list_of_employees
   
    def get_list_of_names_and_social_security_employee_where_vat_is_required(self, for_year , for_month):
        entries = self.vat.internal_get_entries_for_month(for_year=for_year , for_month=for_month , is_required_to_pay_vat=True)
        list_of_employees = []
        for entry in entries:
            social_security_dict = self.social_security.calculate_social_security_employee_by_employee_monthly_entry(entry.Monthly_employee_data_as_object)
            list_of_employees.append(
                { 'social_security_employer' : social_security_dict['total'] , 'name' : '{0} {1}'.format(entry.employee.user.first_name ,entry.employee.user.last_name) })
        return list_of_employees
    
    def get_sum_of_social_security_employer_where_vat_is_required(self, for_year , for_month):
        sum_to_return = 0
        for row in self.get_list_of_names_and_social_security_employer_where_vat_is_required( for_year=for_year , for_month=for_month):
            sum_to_return += row['social_security_employer']
        return sum_to_return

    def get_yearly_employee_report_data(self, employee , for_year):
        income_tax = 0
        social_security = 0
        vat = 0
        sum_of_gross_payment = 0
        months_in_which_got_paid = []
        for x in range(1,13):
            monthly_employee_report = self.monthly_employee_report(employee=employee, for_year=for_year, for_month=x)
            monthly_employee_data = self.getter.get_employee_data_by_month(employee=employee,  for_year=for_year, for_month=x)

            income_tax += monthly_employee_report['income_tax_due_this_month']
            social_security += monthly_employee_report['social_security_employee_due_this_month']
            vat += monthly_employee_report['vat_due_this_month']
            if monthly_employee_data:
                sum_of_gross_payment += monthly_employee_data.gross_payment
                months_in_which_got_paid.append(x)
        
        return {
            'sum_of_income_tax': income_tax,
            'sum_of_social_security': social_security,
            'sum_of_vat': vat,
            'sum_of_gross_payment': sum_of_gross_payment,
            'months_in_which_got_paid': months_in_which_got_paid,
        }

    def get_yearly_income_tax_employer_report(self, for_year):
        #get all employees
        all_employees = self.social_security.internal_get_all_employees()

        #iterate emlolyees
        employees_list = []
        for employee in all_employees:
            yearly_employee_report = self.get_yearly_employee_report_data(employee=employee , for_year=2015)

            entry = {}
            entry['first_name'] = employee.user.first_name
            entry['last_name'] = employee.user.last_name
            entry['government_id'] = employee.government_id            
            entry['sum_of_income_tax'] = yearly_employee_report['sum_of_income_tax']
            entry['sum_input_tax_vat'] = 'sum_input_tax_vat' #sum vat where is_required_to_pay_vat = False
            entry['sum_of_vat_and_gross_payment'] = yearly_employee_report['sum_of_vat'] + yearly_employee_report['sum_of_gross_payment']
            employees_list.append(entry)
             
        #calculate  sum_of_income_tax, sum_input_tax_vat, sum_of_vat_and_gross_payment
        # add to summery
        #

        response_dict = {
            'employees_list': employees_list,
            'income_tax_id':0,
            'sum_of_income_tax_from_all_employees':0,
            'sum_input_tax_vat_from_all_employees':0,
            'sum_of_vat_and_gross_payment_from_all_employees':0,
        }        
        return response_dict

