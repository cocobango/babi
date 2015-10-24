# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0016_monthly_employee_report_data_net'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthly_employee_social_security_report_data',
            old_name='sum_to_calculate_as_upper_social_security_percentage',
            new_name='sum_to_calculate_as_upper_social_security_percentage_employer',
        ),
        migrations.RenameField(
            model_name='monthly_employee_social_security_report_data',
            old_name='diminished_sum',
            new_name='total_employee',
        ),
        migrations.RenameField(
            model_name='monthly_employee_social_security_report_data',
            old_name='standard_sum',
            new_name='total_employer',
        ),
        migrations.RemoveField(
            model_name='monthly_employee_social_security_report_data',
            name='sum_to_calculate_as_lower_social_security_percentage',
        ),
        migrations.RemoveField(
            model_name='monthly_employee_social_security_report_data',
            name='total',
        ),
        migrations.AddField(
            model_name='monthly_employee_social_security_report_data',
            name='diminished_sum_employee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_employee_social_security_report_data',
            name='diminished_sum_employer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_employee_social_security_report_data',
            name='standard_sum_employee',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_employee_social_security_report_data',
            name='standard_sum_employer',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_employee_social_security_report_data',
            name='sum_to_calculate_as_lower_social_security_percentage_employee',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_employee_social_security_report_data',
            name='sum_to_calculate_as_lower_social_security_percentage_employer',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_employee_social_security_report_data',
            name='sum_to_calculate_as_upper_social_security_percentage_employee',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=11),
            preserve_default=False,
        ),
    ]
