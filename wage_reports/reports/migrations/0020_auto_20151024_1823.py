# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0019_remove_locked_months_first_day_in_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthly_employee_social_security_report_data',
            name='health_insurance',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_system_data',
            name='lower_health_insurance_percentage',
            field=models.DecimalField(default=0.031, decimal_places=8, max_digits=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_system_data',
            name='upper_health_insurance_percentage',
            field=models.DecimalField(default=0.05, decimal_places=8, max_digits=16),
            preserve_default=False,
        ),
    ]
