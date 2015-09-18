
from .models import *
from .helpers import *
from .calculations import *


class ReportsMaker(object):
	"""docstring for ReportsMaker"""
	def __init__(self , employer):
		super(ReportsMaker, self).__init__()
		self.data_getter = data_getter()
		self.income_tax = income_tax_calculations(user_id=employer.user.id)
		self.social_security = social_security_calculations(user_id=employer.user.id)
		self.vat = vat_calculations(user_id=employer.user.id)

	def monthly_employee_report(self, employee, for_year, for_month):
		monthly_employee_data = self.data_getter.get_employee_data_by_month(employee=employee,for_year=for_year,for_month=for_month)
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

	def monthly_employer_report(self, for_year, for_month):
		report_data = {
			'social_security': {
				'count_of_employees_that_are_required_to_pay_social_security' : self.social_security.get_count_of_employees_that_are_required_to_pay_social_security_by_employer(for_year , for_month),
	            'sum_of_gross_payment_of_employees_that_are_required_to_pay_social_security': self.social_security.get_sum_of_gross_payment_of_employees_that_are_required_to_pay_social_security_by_employer(for_year , for_month)['my_total'],
	            'sum_of_gross_payment_to_be_paid_at_lower_employer_rate_social_security': self.social_security.get_sum_of_lower_employer_social_security_by_employer(for_year , for_month),
	            'sum_of_gross_payment_to_be_paid_at_lower_employee_rate_social_security': self.social_security.get_sum_of_lower_employee_social_security_by_employer(for_year , for_month),
	            'total_of_social_security_due': self.social_security.get_total_of_social_security_due_by_employer(for_year, for_month),
	            'count_of_employees_that_do_not_exceed_the_social_security_threshold': self.social_security.get_count_of_employees_that_do_not_exceed_the_social_security_threshold_by_employer(for_year, for_month)
			} , 
			'vat': {
				'sum_of_gross_payment_where_no_vat_is_required': self.vat.get_sum_of_gross_payment_where_no_vat_is_required(for_year=for_year , for_month=for_month),
				'count_of_employees_where_no_vat_is_required': self.vat.get_count_of_employees_where_no_vat_is_required(for_year=for_year , for_month=for_month),
				'sum_of_vat_due_where_no_vat_is_required': self.vat.get_sum_of_vat_due_where_no_vat_is_required(for_year=for_year , for_month=for_month)
			} , 
			'income_tax': {
				'count_of_employees_that_got_paid_this_month': self.income_tax.get_count_of_employees_that_got_paid_this_month(for_year=for_year , for_month=for_month),
				'sum_of_gross_payment_and_vat_for_employees_that_got_paid_this_month': self.income_tax.get_sum_of_gross_payment_and_vat_for_employees_that_got_paid_this_month(for_year=for_year , for_month=for_month),
				'sum_of_income_tax':self.income_tax.get_sum_of_income_tax(for_year=for_year , for_month=for_month)
			}
			
		}
		return report_data
	def three_months_employer_report(self, employer, for_year, for_month):
		pass
	def yearly_employee_report(self, employee, for_year):
		pass
	
	def yearly_social_security_employer_report(self, employer, for_year):
		pass

	#856 report
	def yearly_income_tax_employer_report(self, employer, for_year):
		pass