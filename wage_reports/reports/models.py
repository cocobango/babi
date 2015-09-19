import re


from django.db import models
from datetime import datetime 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


from .helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking , calculate_gross_when_cost_or_or_gross_is_set_to_cost
class Employer(models.Model):
    user = models.OneToOneField(User)
    business_id = models.IntegerField()
    income_tax_id = models.IntegerField()
    phone_number = models.BigIntegerField()
    name_of_contact = models.CharField(max_length=200)
    is_required_to_pay_vat = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username

    def is_employer(user):
        try:
            employer = Employer.objects.get(user=user)
            return True
        except Exception as e:
            return False
    def get_employer_from_user(user):
        try:
            employer = Employer.objects.get(user=user)
            return employer
        except Exception as e:
            return False


class Employee(models.Model):
    user = models.OneToOneField(User)
    employer = models.ForeignKey(Employer)
    birthday = models.DateField()
    government_id = models.IntegerField()
    def __str__(self):
        return self.user.username
    


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
    is_employer_the_main_employer = models.BooleanField(default=False)
    gross_payment_from_others = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return str(self.created)

    def save(self, commit=True, *args, **kwargs):
        if commit:
            if self.is_valid_month():
                if self.duplicate_employer_data():
                    self.gross_payment = self.set_gross_payment()
                    super(Monthly_employee_data, self).save(*args, **kwargs)
                    return self
                else:
                    return False
            else:
                return False
        return self
    # @todo check locked months for first entry of users
    def is_valid_month(self ):
        """ 
        Need to check if this entry can be added.
        An employee cannot add to a month that an employer had entered data for
        An employee cannot add after a month is over
        An employee and an employer cannot add to a locked month
        """
        # return False
        if self.entered_by == 'admin':
            return True
        try:
            latest_entry = Monthly_employee_data.objects.select_related('employee__employer').filter(employee=self.employee_id).latest('created')
        except ObjectDoesNotExist:
            latest_entry = {}
        month_for_employee = get_month_in_question_for_employee_locking()
        year_for_employee = get_year_in_question_for_employee_locking()
        if self.entered_by == 'employee':
            if latest_entry:
                if latest_entry.entered_by == 'employer':
                    return False
            if not (self.for_month == month_for_employee and self.for_year == year_for_employee):
                return False
        else:
            month_for_employer = get_month_in_question_for_employer_locking()
            year_for_employer = get_year_in_question_for_employer_locking()
            if not (self.for_month == month_for_employer and self.for_year == year_for_employer):
                if not (self.for_month == month_for_employee and self.for_year == year_for_employee):
                    return False
        is_month_locked = Locked_months.objects.select_related('employer').filter(for_month=self.for_month , for_year=self.for_year, employer=self.employee.employer)
        if is_month_locked:
            return False
        return True

    def duplicate_employer_data(self):
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

    def set_gross_payment(self):
        initial_gross = self.salary + self.general_expenses
        latest_employer_data = Monthly_employer_data.objects.filter(employee=self.employee).order_by('-id')[0]
        if latest_employer_data.gross_or_cost:
            return initial_gross
        monthly_system_data = Monthly_system_data.objects.order_by('-id').filter(for_year=self.for_year , for_month=self.for_month)[0]
        return calculate_gross_when_cost_or_or_gross_is_set_to_cost(cost=initial_gross , lower_employer_social_security_percentage=monthly_system_data.lower_employer_social_security_percentage , upper_employer_social_security_percentage=monthly_system_data.upper_employer_social_security_percentage , social_security_threshold=monthly_system_data.social_security_threshold)

class Monthly_employer_data(models.Model):
    """The information an employer enters each month is called Monthly_employee_data"""
    employee = models.ForeignKey(Employee)
    created = models.DateTimeField(auto_now_add=True , blank=True)
    entered_by = models.CharField(max_length=30 , default='employee')
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


class Locked_months(models.Model):
    """A table of keys specifying which employer has locked which month"""
    employer = models.ForeignKey(Employer)
    for_month = models.IntegerField(default=0) 
    for_year = models.IntegerField(default=0) 
    lock_time = models.DateTimeField(auto_now_add=True , blank=True)
    first_day_in_month = models.DateTimeField(blank=True)
