from django.db import models
from django.contrib.auth.models import User

class Monthly_system_data(models.Model):
    """The parameters that are used for each month's calculations is called Monthly_system_data"""
    created = models.DateTimeField(auto_now_add=True , blank=True)
    for_month = models.IntegerField(default=0) 
    for_year = models.IntegerField(default=0)     
    vat_percentage = models.DecimalField(max_digits=16, decimal_places=8)
    social_security_threshold = models.DecimalField(max_digits=16, decimal_places=8)
    lower_employee_social_security_percentage = models.DecimalField(max_digits=16, decimal_places=8)
    lower_employer_social_security_percentage = models.DecimalField(max_digits=16, decimal_places=8)
    upper_employee_social_security_percentage = models.DecimalField(max_digits=16, decimal_places=8)
    upper_employer_social_security_percentage = models.DecimalField(max_digits=16, decimal_places=8)
    maximal_sum_to_pay_social_security = models.DecimalField(max_digits=11, decimal_places=2)
    income_tax_default = models.DecimalField(max_digits=16, decimal_places=8)

