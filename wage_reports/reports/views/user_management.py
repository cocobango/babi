from datetime import datetime


from django.contrib.auth import logout as logout_function
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse , JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.utils import timezone

from ..forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from ..models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months


from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking

from ..calculations import social_security_calculations , vat_calculations , income_tax_calculations
from ..decorators import user_is_an_employer

from ..view_helpers import *




@login_required
def user_management(request):
    return render(request, 'reports/employer/user_management.html' , { })

@login_required
def add_employee(request):
    if request.method == 'POST':
        form_registration = UserCreateForm(request.POST)
        
        if form_registration.is_valid():
            form_registration.save(commit=False)
            form = EmployeeForm(request.POST)
            if form.is_valid():
                new_user = form_registration.save()
                employee_form_data = form.save(commit=False)
                employer = Employer.objects.get(user=request.user)
                new_employee = Employee(user=new_user , employer=employer , birthday=employee_form_data.birthday , government_id=employee_form_data.government_id)
                new_employee.save()
                return HttpResponseRedirect(reverse('reports:edit_specific_monthly_employer_data' , args=(new_user.id,)))
            else:
                return HttpResponseRedirect(reverse('my_login:messages' , args=('user was not added, employee data was not valid',)))
        else:
            return HttpResponseRedirect(reverse('my_login:messages' , args=('user was not added, user data was not valid',)))
            
    else:
        form_registration = UserCreateForm()
        form = EmployeeForm();
    return render(request, 'reports/employer/add_employee.html' , { 'form' : EmployeeForm , 'form_registration' : form_registration })

@login_required
def view_all_employees(request):
    Employer_obj = Employer.objects.get(user=request.user)
    employees = Employee.objects.filter(employer=Employer_obj)
    return render(request, 'reports/employer/view_all_employees.html' , { 'json' : serializers.serialize('json' , employees) , 'employees' : employees })

@login_required
def toggle_employee_status(request):
    if request.method == 'POST':
        employer = get_object_or_404(Employer , user=request.user)
        # employee = Employee.objects.get(employer=employer , user_id=request.POST['employee_user_id'])
        employee = get_object_or_404(Employee , employer=employer , user_id=request.POST['employee_user_id'])

        if employee.user.is_active:
            employee.user.is_active = False
        else:
            employee.user.is_active = True
        employee.user.save()
        return HttpResponseRedirect(reverse('reports:view_all_employees' , ))
    else:
        return HttpResponseRedirect(reverse('my_login:messages' , args=('Error, this is a POST gateway, not GET',)))
