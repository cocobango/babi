from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Monthly_employee_data, Employee

def enter_employee_monthly_data(request):
    return render(request, 'reports/employee/monthly_entry.html')