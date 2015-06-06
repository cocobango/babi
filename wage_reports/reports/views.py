from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.core import serializers

from .forms import EmployeeForm , EmployeeMonthlyEntryForm , UserCreateForm 
from .models import Monthly_employee_data, Employee , Employer

@login_required
def user_management(request):
    pass

def add_employee(request):
    if request.method == 'POST':
        form_registration = UserCreateForm(request.POST)
        
        if form_registration.is_valid():
            new_user = form_registration.save()
            form = EmployeeForm(request.POST)
            if form.is_valid():
                employee_form_data = form.save(commit=False)
                employer = Employer.objects.get(user=request.user)
                new_employee = Employee(user=new_user , employer=employer , birthday=employee_form_data.birthday , government_id=employee_form_data.government_id)
                new_employee.save()
                return HttpResponseRedirect(reverse('my_login:messages' , args=('user added successfuly',)))
            else:
                return HttpResponseRedirect(reverse('my_login:messages' , args=('user was not added, user data was not valid',)))
        else:
            return HttpResponseRedirect(reverse('my_login:messages' , args=('user was not added, employee data was not valid',)))
            
    else:
        form_registration = UserCreateForm()
        form = EmployeeForm();
    return render(request, 'reports/employee/add_employee.html' , { 'form' : EmployeeForm , 'form_registration' : form_registration })

@login_required
def view_all_employees(request):
    Employer_obj = Employer.objects.get(user=request.user)
    employees = Employee.objects.filter(employer=Employer_obj)
    return render(request, 'reports/employee/view_all_employees.html' , { 'json' : serializers.serialize('json' , employees) , 'employees' : employees })

def neutralize_employee(request):
    pass

def view_history(request):
    pass


def view_all_months(request):
    pass


def view_a_single_month(request):
    pass


def view_report_of_type(request):
    pass

def current_month(request):
    pass

def show_entrees(request):
    pass

def set_as_valid(request):
    pass

def edit_specific_entry(request):
    return render(request, 'reports/employee/monthly_entry.html' , { 'form' : EmployeeForm })


def enter_employer_monthly_data(request):
    pass

@login_required
def index(request):
    return render(request, 'reports/employee/add_employee.html' , { 'form' : EmployeeForm })

def redirect_to_login(request):
    redirect_to_login('/')



def login_destination(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
        	pass
            # Return a 'disabled account' error message
    else:
        return HttpResponseRedirect(reverse('my_login:messages' , args=('invalid login',)))


def login(request):
    pass

