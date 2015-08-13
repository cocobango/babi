from datetime import datetime


from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse , JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.utils import timezone

from .forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from .models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months


from .helpers import is_employer
@login_required
def index(request):
    if is_employer(request.user):
        return render(request, 'reports/employer/index.html' , {})
    else:
        return render(request, 'reports/employee/index.html' , {})


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

def pre_approve_month(request):
    Employer_obj = Employer.objects.get(user=request.user)
    employees = Employee.objects.filter(employer=Employer_obj)
    approved_entries = []
    disapproved_entries = []
    empty_entries = []
    no_recent_entries = []
    for employee in employees:
        try:
            single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
            this_month = timezone.now()
            if single_entry.created.month == this_month.month and single_entry.created.year == this_month.year:
                if single_entry.is_approved:
                    approved_entries.append(single_entry) 
                else:
                    disapproved_entries.append(single_entry)
            else:
                no_recent_entries.append(single_entry)
        except Monthly_employee_data.DoesNotExist:
            empty_entry = { 'employee' : Employee(user = employee.user) , 'has_data' : False }
            empty_entries.append( empty_entry )
    return render(request, 'reports/employer/pre_approve_month.html' , { 'approved_entries' : approved_entries , 'disapproved_entries' : disapproved_entries , 'no_recent_entries' : no_recent_entries , 'empty_entries' : empty_entries })

def approve_this_month(request):
    if request.method == 'POST':
        try:
            now = timezone.now()
            locked_month = Locked_months.objects.select_related('employer').get(for_month=request['for_month'] , for_year=request['for_year'], employer__user=request['user'])
            return HttpResponseRedirect(reverse('my_login:messages' , args=('month allready locked',)))
        except ObjectDoesNotExist:
            locked_month = Locked_months()
    else:
        return HttpResponseRedirect(reverse('my_login:messages' , args=('Error, this is a POST gateway, not GET',)))

def set_as_valid(request):
    if request.method == 'POST':
        try:
            single_entry = Monthly_employee_data.objects.select_related('employee__user').get(pk=request.POST['entry_id'] , employee__user_id=request.POST['employee_user_id'] , employee__employer__user=request.user )
            single_entry.is_approved = True
            single_entry.pk = None
            # Monthly_employee_data.objects.filter( employee__user_id=11 , created__gte=timezone.now().replace(day=1,hour=0, minute=0) ).update(is_approved=False)
            Monthly_employee_data.objects.select_related('employee__user').filter( employee__user_id=request.POST['employee_user_id'] , created__gte=timezone.now().replace(day=1,hour=0, minute=0) ).update(is_approved=False)
            single_entry.created = None
            single_entry.save()
            return JsonResponse({'is_okay':True , 'message' : 'successfully approved entry' , 'data' : single_entry.id})
        except Monthly_employee_data.DoesNotExist:
            return JsonResponse({'is_okay':True , 'message' : 'Error: Failed to approve entry' , 'data' : 'entry was not added, entry %s ,employee_user %s , employer %s' % { request.POST['entry_id'] , request.POST['employee_user_id'] , request.user}})
    else:
        return HttpResponseRedirect(reverse('my_login:messages' , args=('Error, this is a POST gateway, not GET',)))
    

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
        employee = get_object_or_404(Employee , user_id=employee_user_id)
        try:
            single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
            form = EmployeeMonthlyEntryForm(instance=single_entry)
        except Monthly_employee_data.DoesNotExist:
            form = EmployeeMonthlyEntryForm()
        return render(request, 'reports/employee/monthly_entry.html' , { 'form' : form , 'employee_user_id' : employee_user_id })
    


def edit_specific_monthly_employer_data(request, employee_user_id):
    if request.method == 'POST':
        form_entry = EmployerMonthlyEntryForm(request.POST)
        if form_entry.is_valid():
            employer = get_object_or_404(Employer , user=request.user)
            employee = get_object_or_404(Employee , employer=employer , user_id=request.POST['employee_user_id'])
            partial_monthly_entree = form_entry.save(commit=False)
            partial_monthly_entree.employee = employee
            partial_monthly_entree.entered_by = 'employer'
            partial_monthly_entree.save()
            return HttpResponseRedirect(reverse('reports:view_all_employees' ))
        else:
            return HttpResponseRedirect(reverse('my_login:messages' , args=('entry was not added, data was not valid',)))
            
    else:
        employee = get_object_or_404(Employee , user_id=employee_user_id)
        try:
            single_entry = Monthly_employer_data.objects.filter(employee=employee).latest('created')
            form = EmployerMonthlyEntryForm(instance=single_entry)
        except Monthly_employer_data.DoesNotExist:
            form = EmployerMonthlyEntryForm()
        return render(request, 'reports/employer/monthly_entry.html' , { 'form' : form , 'employee_user_id' : employee_user_id })
    

def redirect_to_real_login(request):
    return redirect_to_login('accounts/profile')



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

