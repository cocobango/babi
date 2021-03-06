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
from django.contrib.auth.models import User

from ..forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from ..models import Monthly_employer_data, Monthly_employee_data, Employee, Employer, Locked_months


from ..reports_maker import ReportsMaker

from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking, logger

from ..calculations import social_security_calculations , vat_calculations , income_tax_calculations
from ..decorators import *

from ..view_helpers import *



@login_required
@user_is_an_employer
def show_entries(request , for_year , for_month):
    past_or_current_month = 'past'
    if int(for_month) == int(get_month_in_question_for_employee_locking()):
        past_or_current_month = 'current'

    if int(for_month) not in [int(get_month_in_question_for_employee_locking()), int(get_month_in_question_for_employer_locking())]:
        return render(request, 'reports/general/display_message.html' , { 'headline' : "Month locked" , 'body' : "This month is not in the time range of months available for editing" }) 
    if int(for_year) not in [int(get_year_in_question_for_employee_locking()), int(get_year_in_question_for_employer_locking())]:
        return render(request, 'reports/general/display_message.html' , { 'headline' : "Month locked" , 'body' : "This month is not in the time range of months available for editing" })
    Employer_obj = Employer.objects.get(user=request.user)
    try:
        locked_month = Locked_months.objects.select_related('employer').filter(employer__user=request.user , for_year=for_year , for_month=for_month)[0]
        if locked_month.for_month == for_month and locked_month.for_year == for_year:
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
            
    return render(request, 'reports/employer/show_entries.html' , { 'employees' : employees , 'entries' : entries , 'employees_that_do_not_have_employer_data' : employees_that_do_not_have_employer_data , 'for_year' : for_year , 'for_month' : for_month , 'past_or_current_month':past_or_current_month })

@login_required
def pre_approve_month(request):
    Employer_obj = Employer.objects.get(user=request.user)
    employees = Employee.objects.filter(employer=Employer_obj)
    this_month = timezone.now()
    for_month = get_month_in_question_for_employer_locking()
    for_year = get_year_in_question_for_employer_locking()
    approved_entries = []
    disapproved_entries = []
    empty_entries = []
    no_recent_entries = []
    for employee in employees:
        try:
            single_entry = Monthly_employee_data.objects.filter(employee=employee).latest('created')
            if single_entry.for_month == for_month and single_entry.for_year == for_year:
                if single_entry.is_approved:
                    approved_entries.append(single_entry) 
                else:
                    disapproved_entries.append(single_entry)
            else:
                no_recent_entries.append(single_entry)
        except Monthly_employee_data.DoesNotExist:
            empty_entry = { 'employee' : Employee(user = employee.user) , 'has_data' : False }
            empty_entries.append( empty_entry )
    return render(request, 'reports/employer/pre_approve_month.html' , { 'for_month': for_month , 'for_year': for_year , 'approved_entries' : approved_entries , 'disapproved_entries' : disapproved_entries , 'no_recent_entries' : no_recent_entries , 'empty_entries' : empty_entries })

@login_required
@user_is_an_employer
def approve_this_month(request):
    if request.method == 'POST':
        try:
            now = timezone.now()
            locked_month = Locked_months.objects.select_related('employer__user').get(for_month=request.POST['for_month'] , for_year=request.POST['for_year'], employer__user=request.user)
            return JsonResponse({'is_okay':False , 'message' : 'This month is already locked' , 'data' : None })
        except Locked_months.DoesNotExist:
            if Employer.is_employer(request.user):
                employer = Employer.get_employer_from_user(request.user) 
                locked_month = Locked_months(for_year = request.POST['for_year'] , for_month = request.POST['for_month'], employer = employer)
                locked_month.save()
                return JsonResponse({'is_okay':True , 'message' : 'successfully locked month. you can now get reports for this month' , 'data' : None })
    else:
        return HttpResponseRedirect(reverse('my_login:messages' , args=('Error, this is a POST gateway, not GET',)))

@login_required
@user_is_an_employer
@user_is_a_specific_employer_for_employee(employee_user_id_field_name='employee_user_id')
def set_as_valid(request):
    if request.method == 'POST':
        try:
            single_entry = Monthly_employee_data.objects.select_related('employee__user').get(pk=request.POST['entry_id'] , employee__user_id=request.POST['employee_user_id'] , employee__employer__user=request.user )

            for_year = request.POST['for_year']
            for_month = request.POST['for_month']

            single_entry.is_approved = True
            single_entry.pk = None
            single_entry.for_year = for_year
            single_entry.for_month = for_month
            single_entry.entered_by = 'employer'
            single_entry.created = None

            if single_entry.save():
                employer = Employer.get_employer_from_user(request.user) 
                employee = Employee.get_employee_from_user(request.POST['employee_user_id'])
                reportsMaker = ReportsMaker(employer)
                reportsMaker.populate_calculated_data_for_single_employee(employee=employee, for_year=for_year, for_month=for_month)

                return JsonResponse({'is_okay':True , 'message' : 'successfully approved entry' , 'data' : single_entry.id})
            return JsonResponse({'is_okay':False , 'message' : 'Error: Failed to approve entry, code 4534' , 'data' : 'check permissions of month'})
        except Monthly_employee_data.DoesNotExist:
            return JsonResponse({'is_okay':True , 'message' : 'Error: Failed to approve entry' , 'data' : 'entry was not added, entry {0} ,employee_user {1} , employer {2}'.format(request.POST['entry_id'] , request.POST['employee_user_id'] , request.user)})
    else:
        return HttpResponseRedirect(reverse('my_login:messages' , args=('Error, this is a POST gateway, not GET',)))
    
@login_required
@user_is_an_employer
@user_is_a_specific_employer_for_employee(employee_user_id_field_name='employee_user_id')
def withdraw_approval_of_single_entry(request):
    if request.method == 'POST':
        try:
            single_entry = Monthly_employee_data.objects.select_related('employee__user').get(pk=request.POST['entry_id'] , employee__user_id=request.POST['employee_user_id'] , employee__employer__user=request.user )
            single_entry.is_approved = False
            if single_entry.save():
                return JsonResponse({'is_okay':True , 'message' : 'successfully withdraw approval from entry' , 'data' : single_entry.id})
        except Monthly_employee_data.DoesNotExist:
            pass
        return JsonResponse({'is_okay':False , 'message' : 'Error: Failed to withdraw approval from entry' , 'data' : 'entry was not updated, entry {0} ,employee_user {1} , employer {2}'.format( request.POST['entry_id'] , request.POST['employee_user_id'] , request.user)})
    else:
        return render(request, 'reports/general/display_message.html' , { 'headline' : "Error" , 'body' : "This is a POST gateway, not GET" })   

@login_required
@user_is_an_employer
@user_is_a_specific_employer_for_employee(employee_user_id_arg_number=0, employee_user_id_field_name='employee_user_id')
def edit_specific_entry_by_employer(request , employee_user_id ):
    employee = get_object_or_404(Employee , user_id=employee_user_id)
    error_message = ''
    if request.method == 'POST':
        response = edit_specific_entry_post(request, employee , 'employer')
        if response['is_okay']:
            return HttpResponseRedirect(reverse('reports:show_entries' , kwargs={'for_year':request.POST['for_year'], 'for_month':request.POST['for_month'] } ) )
        else:
            return edit_specific_entry_get(request=request, employee=employee , error_message=response['message'] , action=reverse('reports:edit_specific_entry_by_employer' , kwargs={'employee_user_id':employee_user_id} ), form=response['form'])
    else:
        return edit_specific_entry_get(request=request, employee=employee , error_message=error_message , action=reverse('reports:edit_specific_entry_by_employer' , kwargs={'employee_user_id':employee_user_id} ))
        

@login_required
def edit_specific_entry_by_employee(request):
    employee = get_object_or_404(Employee , user_id=request.user.id)
    error_message = ''
    form = None
    if request.method == 'POST':
        response = edit_specific_entry_post(request, employee , 'employee')
        if response['is_okay']:
            return render(request, 'reports/general/display_message.html' , { 'headline' : "הצלחה" , 'body' : response['message'] })   
        error_message = response['message']
        form = response['form'] 
    return edit_specific_entry_get(request=request, employee=employee , error_message=error_message , action=reverse('reports:edit_specific_entry_by_employee' ), form=form)
#post

# return render(request, 'reports/general/display_message.html' , { 'headline' : "Success" , 'body' : "Your input was received successfully" })



@login_required
@user_is_an_employer
@user_is_a_specific_employer_for_employee(employee_user_id_arg_number=0, employee_user_id_field_name='employee_user_id')
def edit_specific_monthly_employer_data(request, employee_user_id):
    error_message = ''
    if request.method == 'POST':
        form_entry = EmployerMonthlyEntryForm(request.POST)
        if form_entry.is_valid():
            employer = get_object_or_404(Employer , user=request.user)
            employee = get_object_or_404(Employee , employer=employer , user_id=request.POST['employee_user_id'])
            partial_monthly_entree = form_entry.save(commit=False)
            partial_monthly_entree.employee = employee
            partial_monthly_entree.entered_by = 'employer'
            partial_monthly_entree.is_approved = True
            if partial_monthly_entree.save():
                if Monthly_employer_data.objects.filter(employee=employee).count() == 1:
                    employee_user = User.objects.get(id=request.POST['employee_user_id'])
                    employee_user.is_active = True
                    employee_user.save()
                return HttpResponseRedirect(reverse('reports:view_all_employees' ))
        form = form_entry
        error_message = 'המידע לא נקלט במערכת משום שהיה לא תקין'
            
    else:
        employee = get_object_or_404(Employee , user_id=employee_user_id)
        try:
            single_entry = Monthly_employer_data.objects.filter(employee=employee).latest('created')
            form = EmployerMonthlyEntryForm(instance=single_entry)
        except Monthly_employer_data.DoesNotExist:
            form = EmployerMonthlyEntryForm()
    return render(request, 'reports/employer/monthly_entry.html' , { 'form' : form , 'employee_user_id' : employee_user_id, 'error_message': error_message, 'employee':employee })


  