# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0014_monthly_employee_report_data_monthly_employee_social_security_report_data'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='monthly_employee_report_data',
            unique_together=set([('employee', 'for_year', 'for_month')]),
        ),
    ]
