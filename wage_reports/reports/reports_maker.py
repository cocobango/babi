
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

	def monthly_employee_report(self, employee, for_year, for_month):
		monthly_employee_data = self.data_getter.get_employee_data_by_month(employee=employee,for_year=for_year,for_month=for_month)
		return {
			'salary': monthly_employee_data.salary,
            'general_expenses': monthly_employee_data.general_expenses,
            'income_tax_due_this_month': self.income_tax.calculate_income_tax_for_single_employee_for_month(employee=employee, for_year=for_year, for_month=for_month),
            'social_security_employee_due_this_month': 0,
            'vat_due_this_month': 0,
            'monthly_net': 0,
		}

	def monthly_employer_report(self, employer, for_year, for_month):
		pass
	def three_months_employer_report(self, employer, for_year, for_month):
		pass
	def yearly_employee_report(self, employee, for_year):
		pass
	
	def yearly_social_security_employer_report(self, employer, for_year):
		pass

	#856 report
	def yearly_income_tax_employer_report(self, employer, for_year):
		pass