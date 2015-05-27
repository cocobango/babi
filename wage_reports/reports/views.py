from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .forms import EmployeeForm , EmployeeMonthlyEntryForm
from .models import Monthly_employee_data, Employee

def add_employee(request):
    return render(request, 'reports/employee/add_employee.html' , { 'form' : EmployeeForm })

def enter_employee_monthly_data(request):
    return render(request, 'reports/employee/monthly_entry.html' , { 'form' : EmployeeForm })


def enter_employer_monthly_data(request):
    pass

def view_all_emplyees(request):
    pass