from .models import Monthly_employee_data, Employee , Employer , Locked_months


def is_employer(user):
    try:
    	employer = Employer.objects.get(user=user)
    	return True
    except Exception as e:
    	return False
    