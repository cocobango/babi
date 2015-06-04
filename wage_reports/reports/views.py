from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .forms import EmployeeForm , EmployeeMonthlyEntryForm 
from .models import Monthly_employee_data, Employee

@login_required
def user_management(request):
    pass

def add_employee(request):
    return render(request, 'reports/employee/add_employee.html' , { 'form' : EmployeeForm })

def enter_employee_monthly_data(request):
    return render(request, 'reports/employee/monthly_entry.html' , { 'form' : EmployeeForm })


def enter_employer_monthly_data(request):
    pass

@login_required
def index(request):
    return render(request, 'reports/employee/add_employee.html' , { 'form' : EmployeeForm })

def redirect_to_login(request):
    redirect_to_login('/')

def view_all_employees(request):
    pass


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

