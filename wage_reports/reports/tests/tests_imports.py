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
        first_employer = Employer.objects.first()
        reportsMaker = reports_maker.ReportsMaker(employer=first_employer)
        for for_month in range(1 , 4):
            reportsMaker.populate_db_with_calclated_data(for_year=2015, for_month=for_month)

def baseline():
    models = [Employee , Monthly_employee_data , Monthly_employer_data , Monthly_system_data , Monthly_employee_report_data , Monthly_employee_social_security_report_data]
    for model in models:
        model.objects.all().delete()

def clear_reports_data():
    Monthly_employee_report_data.objects.all().delete()
    Monthly_employee_social_security_report_data.objects.all().delete()

def repopulate_db_for_npo_employer():
    clear_reports_data()
    self.myGenerator.generateInitialControlledState()
    first_employer = Employer.objects.first()
    first_employer.is_npo = True
    first_employer.save()
    npo_reports_maker = reports_maker.ReportsMaker(employer=first_employer)
    populate_db_with_the_results_of_calculations_for_all_months()
