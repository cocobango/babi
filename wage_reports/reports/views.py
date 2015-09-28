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

from .forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from .models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months


from .helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking

from .calculations import social_security_calculations , vat_calculations , income_tax_calculations
from .decorators import user_is_an_employer

from .view_helpers import *

@user_is_an_employer
def my_test(request):
    return render(request, 'reports/general/display_message.html' , { 'headline' : "test response:" , 'body' : get_month_in_question_for_employee_locking() })

@login_required
def index(request):
    past_month_dict = {
        'for_year': get_year_in_question_for_employer_locking(),
        'for_month': get_month_in_question_for_employer_locking()
    }
    current_month_dict = {
        'for_year': get_year_in_question_for_employee_locking(),
        'for_month': get_month_in_question_for_employee_locking()
    }
    urls_list = [
            {
                'link': reverse('reports:view_history'),
                'display_text':'View data for past months'
            }
        ]
    if Employer.is_employer(request.user):
        urls_list.extend([
            {
                'link': reverse('reports:user_management'),
                'display_text':'Manage users'
            },
            {
                'link': reverse('reports:show_entries' , kwargs={'for_year':past_month_dict['for_year'],'for_month':past_month_dict['for_month']}),
                'display_text':'Manage past month'
            },
            {
                'link': reverse('reports:show_entries' , kwargs={'for_year':current_month_dict['for_year'],'for_month':current_month_dict['for_month']}),
                'display_text':'Manage current month'
            }
        ])
        return render(request, 'reports/employer/index.html' , {'urls_list':urls_list})
    else:
        return render(request, 'reports/employee/index.html' , {'urls_list':urls_list})


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

@login_required
def view_history(request):
    pass


@login_required
def view_all_months(request):
    pass


@login_required
def view_a_single_month(request):
    pass


@login_required
def view_report_of_type(request , report_type):
    # calculator = social_security_calculations(request.user)
    # for_year = get_year_in_question_for_employer_locking()
    # for_month = get_month_in_question_for_employer_locking()
    # if report_type == 1:

    # response = calculator.get_count_of_employees_that_are_required_to_pay_social_security_by_employer(for_year, for_month) 
    # expected_result = 1
    return render(request, 'reports/general/display_message.html' , { 'headline' : "test response:" , 'body' : str(response) + ' ' + str(expected_result) })

@login_required
def show_entries(request , for_year , for_month):
    year_in_question = for_year
    month_in_question = for_month
    past_or_current_month = 'past'
    lala = 'testing var'
    if int(month_in_question) == int(get_month_in_question_for_employee_locking()):
        past_or_current_month = 'current'
    Employer_obj = Employer.objects.get(user=request.user)
    try:
        locked_month = Locked_months.objects.select_related('employer').filter(employer__user=request.user , for_year=year_in_question , for_month=month_in_question)[0]
        if locked_month.for_month == month_in_question and locked_month.for_year == year_in_question:
            return render(request, 'reports/general/display_message.html' , { 'headline' : "Month locked" , 'body' : "This month is locked for editing. you can view reports on it in the appropriate section" })
    except IndexError:
        pass
    employees = Employee.objects.select_related('user').filter(employer=Employer_obj , employer__user__is_active=True) 
    entries = []
    employees_that_do_not_have_employer_data = []

    for employee in employees:
        if Monthly_employer_data.objects.filter(employee=employee):
            entries.append(get_single_entry_for_a_given_employee_and_month(employee=employee, for_year=for_year, for_month=for_month) )
        else:
            employees_that_do_not_have_employer_data.append(employee)
            
    return render(request, 'reports/employer/show_entries.html' , { 'employees' : employees , 'entries' : entries , 'employees_that_do_not_have_employer_data' : employees_that_do_not_have_employer_data , 'year_in_question' : year_in_question , 'month_in_question' : month_in_question , 'past_or_current_month':past_or_current_month , 'lala':lala })

@login_required
def pre_approve_month(request):
    Employer_obj = Employer.objects.get(user=request.user)
    employees = Employee.objects.filter(employer=Employer_obj)
    this_month = timezone.now()
    month_in_question = get_month_in_question_for_employer_locking()
    year_in_question = get_year_in_question_for_employer_locking()
    approved_entries = []
    disapproved_entries = []
    empty_entries = []
    no_recent_entries = []
    for employee in employees:
        try:
            single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
            if single_entry.for_month == month_in_question and single_entry.for_year == year_in_question:
                if single_entry.is_approved:
                    approved_entries.append(single_entry) 
                else:
                    disapproved_entries.append(single_entry)
            else:
                no_recent_entries.append(single_entry)
        except Monthly_employee_data.DoesNotExist:
            empty_entry = { 'employee' : Employee(user = employee.user) , 'has_data' : False }
            empty_entries.append( empty_entry )
    return render(request, 'reports/employer/pre_approve_month.html' , { 'month_in_question': month_in_question , 'year_in_question': year_in_question , 'approved_entries' : approved_entries , 'disapproved_entries' : disapproved_entries , 'no_recent_entries' : no_recent_entries , 'empty_entries' : empty_entries })

@login_required
def approve_this_month(request):
    if request.method == 'POST':
        try:
            now = timezone.now()
            locked_month = Locked_months.objects.select_related('employer__user').get(for_month=request.POST['for_month'] , for_year=request.POST['for_year'], employer__user=request.user)
            return JsonResponse({'is_okay':False , 'message' : 'This month is already locked' , 'data' : None })
        except Locked_months.DoesNotExist:
            if Employer.is_employer(request.user):
                employer = Employer.get_employer_from_user(request.user) 
                first_day_in_month = datetime( int(request.POST['for_year']), int(request.POST['for_month']), 1)
                locked_month = Locked_months(for_year = request.POST['for_year'] , for_month = request.POST['for_month'], employer = employer , first_day_in_month = first_day_in_month)
                locked_month.save()
                return JsonResponse({'is_okay':True , 'message' : 'successfully locked month. you can now get reports for this month' , 'data' : None })
    else:
        return HttpResponseRedirect(reverse('my_login:messages' , args=('Error, this is a POST gateway, not GET',)))

@login_required
def set_as_valid(request):
    if request.method == 'POST':
        try:
            single_entry = Monthly_employee_data.objects.select_related('employee__user').get(pk=request.POST['entry_id'] , employee__user_id=request.POST['employee_user_id'] , employee__employer__user=request.user )

            year_in_question = request.POST['for_year']
            month_in_question = request.POST['for_month']

            single_entry.is_approved = True
            single_entry.pk = None
            single_entry.for_year = year_in_question
            single_entry.for_month = month_in_question
            single_entry.entered_by = 'employer'

            # Monthly_employee_data.objects.filter( employee__user_id=11 , created__gte=timezone.now().replace(day=1,hour=0, minute=0) ).update(is_approved=False)
            Monthly_employee_data.objects.select_related('employee__user').filter( employee__user_id=request.POST['employee_user_id'] , for_year=year_in_question, for_month=month_in_question).update(is_approved=False)
            single_entry.created = None

            if single_entry.save():
                return JsonResponse({'is_okay':True , 'message' : 'successfully approved entry' , 'data' : single_entry.id})
            return JsonResponse({'is_okay':False , 'message' : 'Error: Failed to approve entry, code 4534' , 'data' : 'check permissions of month'})
        except Monthly_employee_data.DoesNotExist:
            return JsonResponse({'is_okay':True , 'message' : 'Error: Failed to approve entry' , 'data' : 'entry was not added, entry %s ,employee_user %s , employer %s' % { request.POST['entry_id'] , request.POST['employee_user_id'] , request.user}})
    else:
        return HttpResponseRedirect(reverse('my_login:messages' , args=('Error, this is a POST gateway, not GET',)))
    
@login_required
def withdraw_approval_of_single_entry(request):
    if request.method == 'POST':
        try:
            single_entry = Monthly_employee_data.objects.select_related('employee__user').get(pk=request.POST['entry_id'] , employee__user_id=request.POST['employee_user_id'] , employee__employer__user=request.user )
            single_entry.is_approved = False
            single_entry.save()
            return JsonResponse({'is_okay':True , 'message' : 'successfully withdraw approval from entry' , 'data' : single_entry.id})
        except Monthly_employee_data.DoesNotExist:
            return JsonResponse({'is_okay':True , 'message' : 'Error: Failed to withdraw approval from entry' , 'data' : 'entry was not updated, entry %s ,employee_user %s , employer %s' % { request.POST['entry_id'] , request.POST['employee_user_id'] , request.user}})
    else:
        return render(request, 'reports/general/display_message.html' , { 'headline' : "Error" , 'body' : "This is a POST gateway, not GET" })   

@login_required
def edit_specific_entry_by_employer(request , employee_user_id , error_message=''):
    employee = get_object_or_404(Employee , user_id=employee_user_id)
    if request.method == 'POST':
        response = edit_specific_entry_post(request, employee , 'employer')
        if response['is_okay']:
            return HttpResponseRedirect(reverse('reports:show_entries' , kwargs={'for_year':request.POST['for_year'], 'for_month':request.POST['for_month'] } ) )
        else:
            return HttpResponseRedirect(reverse('reports:edit_specific_entry_by_employer' , kwargs={'employee_user_id':employee_user_id} ) )
    else:
        return edit_specific_entry_get(request=request, employee=employee , error_message=error_message , action=reverse('reports:edit_specific_entry_by_employer' , kwargs={'employee_user_id':employee_user_id} ))
        

@login_required
def edit_specific_entry_by_employee(request):
    employee = get_object_or_404(Employee , user_id=request.user.id)
    if request.method == 'POST':
        response = edit_specific_entry_post(request, employee , 'employee')
        if response['is_okay']:
            raise NotImplemented
        else:
            return HttpResponseRedirect(reverse('reports:edit_specific_entry_by_employee' ) )
    else:
        return edit_specific_entry_get(request=request, employee=employee , error_message='' , action=reverse('reports:edit_specific_entry_by_employee' ))
#post

# return render(request, 'reports/general/display_message.html' , { 'headline' : "Success" , 'body' : "Your input was received successfully" })



    
        
        return edit_specific_entry_get(request, employee)

@login_required
def edit_specific_monthly_employer_data(request, employee_user_id):
    if request.method == 'POST':
        form_entry = EmployerMonthlyEntryForm(request.POST)
        if form_entry.is_valid():
            employer = get_object_or_404(Employer , user=request.user)
            employee = get_object_or_404(Employee , employer=employer , user_id=request.POST['employee_user_id'])
            partial_monthly_entree = form_entry.save(commit=False)
            partial_monthly_entree.employee = employee
            partial_monthly_entree.entered_by = 'employer'
            partial_monthly_entree.is_approved = True
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

def logout(request):
    logout_function(request)
    return render(request, 'reports/general/display_message.html' , { 'headline' : "successfully logged out" , 'body' : "" })
    


