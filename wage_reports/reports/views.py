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
    return render(request, 'reports/employer/user_management.html' , { })

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
                return HttpResponseRedirect(reverse('my_login:messages' , args=('user added successfuly',)))
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

def show_entries(request):
    Employer_obj = Employer.objects.get(user=request.user)
    employees = Employee.objects.filter(employer=Employer_obj)
    entries = []
    for employee in employees:
        try:
            single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
            single_entry.has_data = True
            entries.append(single_entry) 
        except Monthly_employee_data.DoesNotExist:
            empty_entry = { 'employee' : Employee(user = employee.user) , 'has_data' : False }
            entries.append( empty_entry )
        
    
    return render(request, 'reports/employer/show_entries.html' , { 'employees' : employees , 'entries' : entries })

def pre_aprove_month(request):
    pass

def set_as_valid(request):
    pass

def edit_specific_entry(request , employee_user_id):
    if request.method == 'POST':
        form_entry = EmployeeMonthlyEntryForm(request.POST)
        
        if form_entry.is_valid():
            employer = get_object_or_404(Employer , user=request.user)
            employee = get_object_or_404(Employee , employer=employer , user_id=request.POST['employee_user_id'])

            partial_monthly_entree = form_entry.save(commit=False)
            partial_monthly_entree.employee = employee
            partial_monthly_entree.entered_by = 'employer'
            partial_monthly_entree.save()
            return HttpResponseRedirect(reverse('reports:show_entries' ))
        else:
            return HttpResponseRedirect(reverse('my_login:messages' , args=('entry was not added, data was not valid',)))
            
    else:
        form_registration = UserCreateForm()
        form = EmployeeForm();
    return render(request, 'reports/employer/monthly_entry.html' , { 'form' : EmployeeMonthlyEntryForm , 'employee_user_id' : employee_user_id })


def enter_employer_monthly_data(request):
    pass

@login_required
def index(request):
    return render(request, 'reports/employer/add_employee.html' , { 'form' : EmployeeForm })

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

