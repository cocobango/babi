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
from django.contrib.auth.decorators import user_passes_test

from ..forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from ..models import Monthly_employer_data, Monthly_employee_data, Monthly_system_data, Employee , Employer , Locked_months , Monthly_employee_report_data , Monthly_employee_social_security_report_data



from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking, get_quarter_from_month, logger

from ..calculations import social_security_calculations , vat_calculations , income_tax_calculations
from ..decorators import *

from ..view_helpers import *

from ..reports_maker import ReportsMaker

@login_required
def view_history(request, user_id):
    logger.debug('employer') 
    data = {'user_id':user_id}
    employer = Employer.get_employer_from_user(user_id)
    logger.debug(employer)
    data['is_employer'] = employer
    return render(request, 'reports/view_history/index.html', data)

@login_required
@user_is_an_employer_or_admin
def view_history_as(request):
    data = {}
    if request.user.is_superuser:
        data['employers_list'] = Employer.objects.all()
        data['employees_list'] = Employee.objects.all()
    employer = Employer.get_employer_from_user(request.user)
    if employer:
        data['employees_list'] = Employee.objects.filter(employer=employer)
    
    return render(request, 'reports/view_history/view_history_as.html', data)


# monthly employee report
@login_required
def view_monthly_employee_report_list(request, employee_user_id):
    employer, employee = get_employer_and_employee(request, employee_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee=employee.id).values('for_year').distinct()
    return render(request, 'reports/employee/monthly_report_list_all_years.html' , { 'employer':employer, 'reports_list':reports_list, 'user_id':employee_user_id})


@login_required
def view_monthly_employee_report_list_by_year(request, employee_user_id, for_year):
    employer, employee = get_employer_and_employee(request, employee_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee=employee.id).values('for_month').distinct() 
    return render(request, 'reports/employee/monthly_report_list_year.html' , { 'employer':employer, 'for_year':for_year, 'reports_list':reports_list, 'user_id':employee_user_id})


@login_required
def view_monthly_employee_report(request, employee_user_id, for_year, for_month):
    employer, employee = get_employer_and_employee(request, employee_user_id)
    is_month_locked = Locked_months.objects.filter(for_month=for_month , for_year=for_year, employer=employer)
    reportsMaker = ReportsMaker(employer)
    report = reportsMaker.monthly_employee_report(employee=employee, for_year=for_year, for_month=for_month)
    return render(request, 'reports/employee/monthly_report_output.html' , { 'report':report, 'employer':employer, 'employee':employee, 'for_year':for_year, 'for_month':for_month, 'is_month_locked':is_month_locked })



# monthly employer report
@login_required
def view_monthly_employer_report_list(request, employer_user_id):
    employer = get_employer(request, employer_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee__employer_id=employer.id).values('for_year').distinct()
    return render(request, 'reports/employer/monthly_report_list_all_years.html' , { 'employer':employer, 'reports_list':reports_list, 'user_id':employer_user_id})

@login_required
def view_monthly_employer_report_list_by_year(request, employer_user_id, for_year):
    employer = get_employer(request, employer_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee__employer_id=employer.id, for_year=for_year).values('for_month').distinct() 
    return render(request, 'reports/employer/monthly_report_list_year.html' , { 'employer':employer, 'for_year':for_year, 'reports_list':reports_list, 'user_id':employer_user_id})

@login_required
def view_monthly_employer_report(request, employer_user_id, for_year, for_month):
    employer = get_employer(request, employer_user_id)
    is_month_locked = Locked_months.objects.filter(for_month=for_month , for_year=for_year, employer=employer)
    reportsMaker = ReportsMaker(employer)
    report = reportsMaker.monthly_employer_report(for_year=for_year, for_month=for_month)
    return render(request, 'reports/employer/monthly_report_output.html' , { 'report':report, 'employer':employer, 'for_year':for_year, 'for_month':for_month, 'is_month_locked':is_month_locked })


# quarterly_social_security_report
@login_required
def view_quarterly_social_security_report_list(request, employer_user_id):
    employer = get_employer(request, employer_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee__employer_id=employer.id).values('for_year').distinct()
    return render(request, 'reports/employer/quarterly_report_list_all_years.html' , { 'employer':employer, 'reports_list':reports_list, 'user_id':employer_user_id})

@login_required
def view_quarterly_social_security_report_list_by_year(request, employer_user_id, for_year):
    employer = get_employer(request, employer_user_id)
    unparsed_reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee__employer_id=employer.id, for_year=for_year).values('for_month').distinct() 
    main_months = [1,4,7,10]
    quarters_to_display = set()
    for month in unparsed_reports_list:
        quarters_to_display.add(get_quarter_from_month(month['for_month']))
    
    return render(request, 'reports/employer/quarterly_report_list_year.html' , { 'employer':employer, 'for_year':for_year, 'quarters_to_display':quarters_to_display, 'user_id':employer_user_id})

@login_required
def view_quarterly_social_security_report(request, employer_user_id, for_year, for_month):
    for_year = int(for_year)
    for_month = int(for_month)
    employer = get_employer(request, employer_user_id)
    is_month_locked = Locked_months.objects.filter(for_month=for_month , for_year=for_year, employer=employer)
    reportsMaker = ReportsMaker(employer)
    report = reportsMaker.quarterly_social_security_report(for_year=for_year, for_month=for_month)
    return render(request, 'reports/employer/quarterly_social_security_report_output.html' , { 'report':report, 'employer':employer, 'for_year':for_year, 'for_month':for_month, 'is_month_locked':is_month_locked })



# yearly employee report
@login_required
def view_yearly_employee_report_list(request, employee_user_id):
    employer, employee = get_employer_and_employee(request, employee_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee=employee.id).values('for_year').distinct()
    return render(request, 'reports/employee/yearly_report_list_all_years.html' , { 'employer':employer, 'reports_list':reports_list, 'user_id':employee_user_id})

@login_required
def view_yearly_employee_report(request, employee_user_id, for_year):
    employer, employee = get_employer_and_employee(request, employee_user_id)
    is_year_locked = Locked_months.objects.filter(for_year=for_year, employer=employer)
    reportsMaker = ReportsMaker(employer)
    report = reportsMaker.yearly_employee_report(employee=employee, for_year=for_year)
    return render(request, 'reports/employee/yearly_report_output.html' , { 'report':report, 'employer':employer, 'employee':employee, 'for_year':for_year, 'is_year_locked':is_year_locked })





# yearly employer report (856)
@login_required
def view_yearly_employer_report_list(request, employer_user_id):
    employer = get_employer(request, employer_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee__employer_id=employer.id).values('for_year').distinct()
    return render(request, 'reports/employer/yearly_report_list_all_years.html' , { 'employer':employer, 'reports_list':reports_list, 'user_id':employer_user_id})

@login_required
def view_yearly_employer_report(request, employer_user_id, for_year):
    employer = get_employer(request, employer_user_id)
    is_year_locked = Locked_months.objects.filter(for_year=for_year, employer=employer)
    reportsMaker = ReportsMaker(employer) 
    report = reportsMaker.yearly_income_tax_employer_report(for_year=for_year)
    return render(request, 'reports/employer/yearly_report_output.html' , { 'report':report, 'employer':employer, 'for_year':for_year, 'is_year_locked':is_year_locked })



# internal reports

# monthly output report
@login_required
def view_monthly_output_report_list(request, employer_user_id):
    employer = get_employer(request, employer_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee__employer_id=employer.id).values('for_year').distinct()
    return render(request, 'reports/employer/monthly_output_report_list_all_years.html' , { 'employer':employer, 'reports_list':reports_list, 'user_id':employer_user_id})

@login_required
def view_monthly_output_report_list_by_year(request, employer_user_id, for_year):
    employer = get_employer(request, employer_user_id)
    reports_list = Monthly_employee_report_data.objects.select_related('employee').filter(employee__employer_id=employer.id, for_year=for_year).values('for_month').distinct() 
    return render(request, 'reports/employer/monthly_output_report_list_year.html' , { 'employer':employer, 'for_year':for_year, 'reports_list':reports_list, 'user_id':employer_user_id})

@login_required
def view_monthly_output_report(request, employer_user_id, for_year, for_month):
    employer = get_employer(request, employer_user_id)
    is_month_locked = Locked_months.objects.filter(for_month=for_month , for_year=for_year, employer=employer)
    reportsMaker = ReportsMaker(employer)
    report = reportsMaker.monthly_output_report(for_year=for_year, for_month=for_month)
    return render(request, 'reports/employer/monthly_output_report_output.html' , { 'report':report, 'employer':employer, 'for_year':for_year, 'for_month':for_month, 'is_month_locked':is_month_locked })





