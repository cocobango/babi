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
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from ..forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from ..models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months


from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking

from ..calculations import social_security_calculations , vat_calculations , income_tax_calculations
from ..decorators import *

from ..view_helpers import *

from ..reports_maker import ReportsMaker

@login_required
def view_history(request):
    data = {}
    try:
        employee = Employee.objects.get(user=request.user.id)
        data['employee_id'] = employee.id
    except ObjectDoesNotExist:
        pass
    try:
        employer = Employer.objects.get(user=request.user.id)
        data['employer_id'] = employer.id
    except ObjectDoesNotExist:
        pass
    return render(request, 'reports/view_history/index.html' , data)


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
def view_monthly_employee_report(request, employee_user_id, for_year, for_month):
    employee = get_object_or_404(Employee , user_id=employee_user_id)
    employer = get_object_or_404(Employer , id=employee.employer.id)
    if request.user.id not in [employee.user.id, employer.user.id] and not request.user.is_superuser:
        raise PermissionDenied
    is_month_locked = Locked_months.objects.filter(for_month=for_month , for_year=for_year, employer=employer)
    reportsMaker = ReportsMaker(employer)
    report = reportsMaker.monthly_employee_report(employee=employee, for_year=for_year, for_month=for_month)
    return render(request, 'reports/employee/monthly_report_output.html' , { 'report':report, 'employer':employer, 'employee':employee, 'for_year':for_year, 'for_month':for_month, 'is_month_locked':is_month_locked })


@login_required
def view_monthly_employer_report(request, employer_user_id, for_year, for_month):
    employer = get_object_or_404(Employer , user_id=employer_user_id)
    if employer.user.id !=  request.user.id and not request.user.is_superuser:
        raise PermissionDenied
    is_month_locked = Locked_months.objects.filter(for_month=for_month , for_year=for_year, employer=employer)
    reportsMaker = ReportsMaker(employer)
    report = reportsMaker.monthly_employer_report(for_year=for_year, for_month=for_month)
    return render(request, 'reports/employer/monthly_report_output.html' , { 'report':report, 'employer':employer, 'for_year':for_year, 'for_month':for_month, 'is_month_locked':is_month_locked })


