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
