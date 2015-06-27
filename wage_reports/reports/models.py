from django.db import models
from datetime import datetime 

from django.contrib.auth.models import User

class Employer(models.Model):
    user = models.OneToOneField(User)
    business_id = models.IntegerField()
    income_tax_id = models.IntegerField()
    phone_number = models.BigIntegerField()
    name_of_contact = models.CharField(max_length=200)
    is_required_to_pay_vat = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username


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
    travel_expenses = models.DecimalField(max_digits=11, decimal_places=2)
    gross_or_cost = models.BooleanField(default=True)
    is_required_to_pay_social_security = models.BooleanField(default=True)
    is_employer_the_main_employer = models.BooleanField(default=True)
    gross_payment_from_others = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return str(self.created)

    def save(self, commit=True, *args, **kwargs):
        if commit:
            if self.is_valid_month():
                super(Monthly_employee_data, self).save(*args, **kwargs)
                return self
            else:
                return False
        return monthly_employee_data
    # @todo check locked months
    def is_valid_month(self ):
        """ 
        Need to check if this entry can be added.
        An employee cannot add to a month that an employer had entered data for
        An employee cannot add after a month is over
        An employee and an employer cannot add to a locked month
        """
        # return False
        latest_entry = Monthly_employee_data.objects.select_related('employee__employer').filter(employee=self.employee_id).latest('created')
        if latest_entry.entered_by == 'employee':
            if latest_entry.entered_by == 'employer':
                return False
            now = timezone.now()
            if not (latest_entry.created.month == now.month and latest_entry.created.year == now.year):
                return False
        is_month_locked = Locked_months.objects.select_related('employer').filter(for_month=self.for_month , for_year=self.for_year, employer=latest_entry.employee.employer)
        if is_month_locked:
            return False
        return True

class Monthly_employer_data(models.Model):
    """The information an employer enters each month is called Monthly_employee_data"""
    monthly_employee_data = models.OneToOneField(Monthly_employee_data)
    created = models.DateTimeField(default=datetime.now , blank=True)
    is_required_to_pay_vat = models.BooleanField(default=True)
    is_required_to_pay_income_tax = models.BooleanField(default=True)
    lower_tax_threshold = models.DecimalField(max_digits=11, decimal_places=2)
    upper_tax_threshold = models.DecimalField(max_digits=11, decimal_places=2)
    income_tax_threshold = models.DecimalField(max_digits=11, decimal_places=2)
    exact_income_tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    

class Monthly_system_data(models.Model):
    """The parameters that are used for each month's calculations is called Monthly_system_data"""
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    social_security_threshold = models.DecimalField(max_digits=11, decimal_places=2)
    lower_employee_social_security_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    lower_employer_social_security_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    upper_employee_social_security_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    upper_employer_social_security_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    maximal_sum_to_pay_social_security = models.DecimalField(max_digits=11, decimal_places=2)
    income_tax_default = models.DecimalField(max_digits=11, decimal_places=2)


class Locked_months(models.Model):
    """A table of keys specifying which employer has locked which month"""
    employer = models.ForeignKey(Employer)
    for_month = models.IntegerField(default=0) 
    for_year = models.IntegerField(default=0) 
    lock_time = models.DateTimeField(auto_now_add=True , blank=True)
