from django.db import models
from django.contrib.auth.models import User

from .locked_months import Locked_months

from .employee import Employee
from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_gross_when_cost_or_or_gross_is_set_to_cost

class Monthly_employer_data(models.Model):
    """The information an employer enters each month is called Monthly_employee_data"""
    employee = models.ForeignKey(Employee)
    created = models.DateTimeField(auto_now_add=True , blank=True)
    entered_by = models.CharField(max_length=30 , default='employer')
    is_approved = models.BooleanField(default=False)
    for_month = models.IntegerField(default=0) 
    for_year = models.IntegerField(default=0) 
    is_required_to_pay_vat = models.BooleanField(default=True)
    is_required_to_pay_income_tax = models.BooleanField(default=True)
    lower_tax_threshold = models.DecimalField(max_digits=11, decimal_places=2)
    upper_tax_threshold = models.DecimalField(max_digits=11, decimal_places=2)
    income_tax_threshold = models.DecimalField(max_digits=11, decimal_places=2)
    exact_income_tax_percentage = models.DecimalField(max_digits=16, decimal_places=8)
    gross_or_cost = models.BooleanField(default=True) #gross is true

    def save(self, commit=True, *args, **kwargs):
        if commit:
            if self.is_valid_month():
                Monthly_employer_data.objects.filter(employee=self.employee , for_month=self.for_month, for_year=self.for_year).update(is_approved=False)
                super(Monthly_employer_data, self).save(*args, **kwargs)
                return self
            else:
                return False
        return self

    def is_valid_month(self):
        if self.entered_by == 'admin':
            return True
        is_month_locked = Locked_months.objects.filter(for_month=self.for_month , for_year=self.for_year, employer=self.employee.employer)
        if is_month_locked:
            return False
        return True
