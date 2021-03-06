from datetime import datetime


from django.contrib.auth.views import login
from django.contrib.auth import logout as logout_function
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse , JsonResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test


from ..forms import EmployeeForm , EmployeeMonthlyEntryForm , EmployerMonthlyEntryForm , UserCreateForm 
from ..models import Monthly_employer_data, Monthly_employee_data, Employee , Employer , Locked_months

from ..helpers import get_month_in_question_for_employer_locking , get_year_in_question_for_employer_locking , get_month_in_question_for_employee_locking , get_year_in_question_for_employee_locking

from ..calculations import social_security_calculations , vat_calculations , income_tax_calculations
from ..decorators import *

from ..view_helpers import *

from ..reports_maker import ReportsMaker

def landing_page(request):
    return render(request, 'reports/general/display_message.html' , { 'headline' : "עמוד הבית של יובל קפלן רואה חשבון" , 'body' : 'index page' })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def store_data(request):
    employer = get_object_or_404(Employer , id=request.POST['employer_id'])
    reportsMaker = ReportsMaker(employer)
    reportsMaker.populate_db_with_calclated_data(for_year=request.POST['for_year'], for_month=request.POST['for_month'])
    return render(request, 'reports/general/display_message.html' , { 'headline' : "test response:" , 'body' : 'data stored for year-{for_year}, month-{for_month}, employer-{employer}'.format(for_year=request.POST['for_year'], for_month=request.POST['for_month'], employer=employer) })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def store_data_gui(request):
    return render(request, 'reports/admin/store_data_gui.html' )
 
def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('reports:index'))
    return login(request, *args, **kwargs)

@user_is_an_employer
def my_test(request):
    return render(request, 'test.html' , { 'headline' : "test response:" , 'body' : get_month_in_question_for_employee_locking() })

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
    return render(request, 'reports/general/index.html', {
        'past_year':past_month_dict['for_year'],
        'current_year':current_month_dict['for_year'],
        'past_month':past_month_dict['for_month'], 
        'current_month':current_month_dict['for_month'], 
    })


def logout(request):
    logout_function(request)
    return HttpResponseRedirect(reverse('main_login'))
    


