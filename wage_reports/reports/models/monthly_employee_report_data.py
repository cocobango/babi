from django.db import models
from . import Employee

class Monthly_employee_report_data(models.Model):
    """The information an employee enters each month is called Monthly_employee_data"""
    employee = models.ForeignKey(Employee)
    created = models.DateTimeField(auto_now_add=True , blank=True)
    entered_by = models.CharField(max_length=30 , default='automatic')
    for_month = models.IntegerField(default=0) 
    for_year = models.IntegerField(default=0) 
    income_tax = models.DecimalField(max_digits=11, decimal_places=2) 
    vat = models.DecimalField(max_digits=11, decimal_places=2)
    input_tax_vat = models.DecimalField(max_digits=11, decimal_places=2)
    net = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return str(self.created)

    class Meta:
        unique_together = ("employee", "for_year", "for_month")
