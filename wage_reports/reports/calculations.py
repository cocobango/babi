from .models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months

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

