# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations ,connection
from django.utils import timezone

# def ready_made_data_for_

def plant_employee_data(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Monthly_employee_data = apps.get_model("reports", "Monthly_employee_data")
    Monthly_employer_data = apps.get_model("reports", "Monthly_employer_data")
    Employee = apps.get_model("reports", "Employee")
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE reports_locked_months")

    employee = Employee.objects.get(id=1)
    qe = Monthly_employee_data(employee=employee , entered_by='employer' , is_approved=True, for_month=1 , for_year=2015 , gross_payment=5000 , salary=4500 , general_expenses=500 , gross_or_cost=True , is_required_to_pay_social_security=True , is_employer_the_main_employer=True , gross_payment_from_others=1000 )
    qe.save()
    qr = Monthly_employer_data(employee=employee , entered_by='employer' , is_approved=True , for_month=1 , for_year=2015 , is_required_to_pay_vat=True , is_required_to_pay_income_tax=False , lower_tax_threshold=0.1 , upper_tax_threshold=0.2 , income_tax_threshold=1 , exact_income_tax_percentage=0 )
    qr.save()


def truncate_tables(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE reports_monthly_employee_data")
    cursor.execute("TRUNCATE TABLE reports_monthly_employer_data")

    # Locked_months = apps.get_model("reports", "Locked_months")
    # Locked_months.objects.all.delete()

def do_nothing(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_auto_20150829_0650'),
    ]

    operations = [
        migrations.RunPython(plant_employee_data , truncate_tables),
    ]
