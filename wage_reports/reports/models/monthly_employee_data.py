import re


from django.db import models
from datetime import datetime 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from .monthly_employer_data import Monthly_employer_data
from .monthly_system_data import Monthly_system_data
from .locked_months import Locked_months
from .employee import Employee
from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_gross_when_cost_or_or_gross_is_set_to_cost


class Monthly_employee_data(models.Model):
    """The information an employee enters each month is called Monthly_employee_data"""
    employee = models.ForeignKey(Employee)
    created = models.DateTimeField(auto_now_add=True , blank=True)
    entered_by = models.CharField(max_length=30 , default='employee')
    is_approved = models.BooleanField(default=False)
    for_month = models.IntegerField(default=0) 
    for_year = models.IntegerField(default=0) 
    gross_payment = models.DecimalField(max_digits=11, decimal_places=2)
    salary = models.DecimalField(max_digits=11, decimal_places=2)
    general_expenses = models.DecimalField(max_digits=11, decimal_places=2)
    is_required_to_pay_social_security = models.BooleanField(default=True)
    is_elderly = models.BooleanField(default=False)
    is_employer_the_main_employer = models.BooleanField(default=False)
    gross_payment_from_others = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return str(self.created)

    def save(self, commit=True, *args, **kwargs):
        if commit:
            if self.is_valid_month():
                if self.duplicate_employer_data():
                    self.gross_payment = self.get_gross_payment()
                    Monthly_employee_data.objects.filter(employee=self.employee , for_month=self.for_month, for_year=self.for_year).update(is_approved=False)
                    super(Monthly_employee_data, self).save(*args, **kwargs)
                    return self
                else:
                    return False #'message':'no employer data exist'
            else:
                return False # 'message':is_valid_month_response['message']
        return self
    # @todo check locked months for first entry of users
    def is_valid_month(self ):
        """ 
        Need to check if this entry can be added.
        An employee cannot add to a month that an employer had entered data for
        An employee cannot add after a month is over
        An employee and an employer cannot add to a locked month
        """
        if self.entered_by == 'admin':
            return True
        try:
            latest_entry = Monthly_employee_data.objects.select_related('employee__employer').filter(employee=self.employee_id , for_year=self.for_year , for_month=self.for_month).latest('created')
        except ObjectDoesNotExist:
            latest_entry = False
        month_for_employee = get_month_in_question_for_employee_locking()
        year_for_employee = get_year_in_question_for_employee_locking()
        if self.entered_by == 'employee':
            if latest_entry:
                if latest_entry.entered_by in ('employer', 'admin'):
                    # return {'is_okay': False , 'message':'Data already entered by employer for this month. Cannot add data from employee'}
                    return False
            if not (self.for_month == month_for_employee and self.for_year == year_for_employee):
                return False
        else: # (entered_by: employer)
            month_for_employer = get_month_in_question_for_employer_locking()
            year_for_employer = get_year_in_question_for_employer_locking()
            if not (int(self.for_month) == month_for_employer and int(self.for_year) == year_for_employer):
                if not (int(self.for_month) == month_for_employee and int(self.for_year) == year_for_employee):
                    # return {'is_okay': False , 'message':'month is not of employer and not of employee. month is: {0}. year is: {1}. for employee month is: {2}'.format(self.for_month , self.for_year , 'month_for_employee')}
                    return False
        is_month_locked = Locked_months.objects.select_related('employer').filter(for_month=self.for_month , for_year=self.for_year, employer=self.employee.employer)
        if is_month_locked:
            return False
        return True

    def duplicate_employer_data(self):
        try:
            Monthly_employer_data.objects.filter(employee=self.employee, for_year=self.for_year, for_month=self.for_month, is_approved=True)[0]
            return True
        except IndexError:
            pass

        try:
            latest_employer_data = Monthly_employer_data.objects.filter(employee=self.employee).order_by('-id')[0]
        except IndexError:
            return False
        latest_employer_data.for_month = self.for_month
        latest_employer_data.for_year = self.for_year
        latest_employer_data.pk = None
        latest_employer_data.is_approved = True
        latest_employer_data.save()
        return True

    def get_gross_payment(self):
        initial_gross = self.salary + self.general_expenses
        latest_employer_data = Monthly_employer_data.objects.filter(employee=self.employee).order_by('-id')[0]
        if latest_employer_data.gross_or_cost:
            return initial_gross
        monthly_system_data = Monthly_system_data().get_relevant(for_year=self.for_year , for_month=self.for_month)
        return calculate_gross_when_cost_or_or_gross_is_set_to_cost(cost=initial_gross , lower_employer_social_security_percentage=monthly_system_data.lower_employer_social_security_percentage , upper_employer_social_security_percentage=monthly_system_data.upper_employer_social_security_percentage , social_security_threshold=monthly_system_data.social_security_threshold)

