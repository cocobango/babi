from decimal import *
getcontext().prec = 6
import json
import unittest

from django.test import TestCase , Client
from django.utils import timezone

from reports.models import Employer , Employee , Monthly_employee_data , Monthly_employer_data , Monthly_system_data , Monthly_employee_report_data , Monthly_employee_social_security_report_data
from django.contrib.auth.models import User
from .. import factories , helpers , reports_maker
from ..calculations import *

def populate_db_with_the_results_of_calculations_for_all_months():
    first_employer = Employer.objects.order_by('-id')[0]
    cross = cross_calculations(user_id=first_employer.user.id)
    for employee in first_employer.employee_set.all():
        for for_month in range(1 , 4):
            cross.monthly_employee_report_to_db(employee=employee,for_year=2015,for_month=for_month)