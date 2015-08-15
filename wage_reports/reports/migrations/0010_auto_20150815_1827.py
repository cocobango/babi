# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0009_locked_months_first_day_in_month'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthly_employee_data',
            old_name='travel_expenses',
            new_name='general_expenses',
        ),
        migrations.AddField(
            model_name='monthly_employee_data',
            name='salary',
            field=models.DecimalField(default=7000, decimal_places=2, max_digits=11),
            preserve_default=False,
        ),
    ]
