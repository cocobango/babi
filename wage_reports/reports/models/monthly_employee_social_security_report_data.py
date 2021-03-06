from django.db import models
from . import Monthly_employee_report_data

class Monthly_employee_social_security_report_data(models.Model):
    """The information an employee enters each month is called Monthly_employee_data"""
    monthly_employee_report_data = models.OneToOneField(Monthly_employee_report_data)
    sum_to_calculate_as_lower_social_security_percentage_employee = models.DecimalField(max_digits=11, decimal_places=2)
    sum_to_calculate_as_upper_social_security_percentage_employee = models.DecimalField(max_digits=11, decimal_places=2)
    diminished_sum_employee = models.DecimalField(max_digits=11, decimal_places=2)
    standard_sum_employee = models.DecimalField(max_digits=11, decimal_places=2)
    health_insurance = models.DecimalField(max_digits=11, decimal_places=2)
    total_employee = models.DecimalField(max_digits=11, decimal_places=2)

    sum_to_calculate_as_lower_social_security_percentage_employer = models.DecimalField(max_digits=11, decimal_places=2)
    sum_to_calculate_as_upper_social_security_percentage_employer = models.DecimalField(max_digits=11, decimal_places=2)
    diminished_sum_employer = models.DecimalField(max_digits=11, decimal_places=2)
    standard_sum_employer = models.DecimalField(max_digits=11, decimal_places=2)
    total_employer = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return str(self.monthly_employee_report_data)
