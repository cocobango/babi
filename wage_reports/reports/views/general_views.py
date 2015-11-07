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

from ..reports_maker import ReportsMaker

@login_required
def store_data(request, employer_id, for_year, for_month):
    employer = get_object_or_404(Employer , id=employer_id)
    reportsMaker = ReportsMaker(employer)
    reportsMaker.populate_db_with_calclated_data(for_year=for_year, for_month=for_month)
    return render(request, 'reports/general/display_message.html' , { 'headline' : "test response:" , 'body' : 'data stored for year-{for_year}, month-{for_month}, employer-{employer}'.format(for_year=for_year, for_month=for_month, employer=employer) })

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



  
def redirect_to_real_login(request):
    return redirect_to_login('accounts/profile')

def logout(request):
    logout_function(request)
    return render(request, 'reports/general/display_message.html' , { 'headline' : "successfully logged out" , 'body' : "" })
    


