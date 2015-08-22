from decimal import *

from django.db.models import Count, Min, Sum, Avg
from .models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months

from .helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_social_security_employer , calculate_social_security_employee , calculate_income_tax , calculate_output_tax , calculate_monthly_net

class social_security_calculations(object):
	"""docstring for social_security_calculations"""
	def __init__(self, user_id):
		super(social_security_calculations, self).__init__()
		self.user_id = user_id
		if Employer.is_employer(user_id):
			self.employer = Employer.get_employer_from_user(user_id)
		# self.
	#employer
	def get_count_of_employees_that_are_required_to_pay_social_security_by_employer(self , for_year, for_month):
		return Monthly_employee_data.objects.select_related('employee').filter(is_required_to_pay_social_security=True, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month).count()

	def get_sum_of_gross_payment_of_employees_that_are_required_to_pay_social_security_by_employer(self , for_year, for_month):
		return Monthly_employee_data.objects.select_related('employee').filter(is_required_to_pay_social_security=True, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month).aggregate(my_total = Sum('gross_payment'))
	def get_sum_of_lower_employee_social_security_by_employer(self , for_year, for_month):
		sum_to_return = 0
		entries = Monthly_employee_data.objects.select_related('employee').filter(is_required_to_pay_social_security=True, employee__employer=self.employer, is_approved=True, for_year=for_year, for_month=for_month)
		for entry in entries:
			# return entry.id
			response = calculate_social_security_employee(overall_gross=entry.gross_payment,social_security_threshold=5500,lower_employee_social_security_percentage=Decimal(0.033),upper_employee_social_security_percentage=Decimal(0.12),is_required_to_pay_social_security=entry.is_required_to_pay_social_security, is_employer_the_main_employer=entry.is_employer_the_main_employer, gross_payment_from_others=2000)
			sum_to_return += response['sum_to_calculate_as_lower_social_security_percentage']
		return sum_to_return

