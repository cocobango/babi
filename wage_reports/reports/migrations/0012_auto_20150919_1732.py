# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0011_auto_20150829_0650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthly_employee_data',
            name='gross_or_cost',
        ),
        migrations.AddField(
            model_name='monthly_employer_data',
            name='gross_or_cost',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='monthly_employee_data',
            name='is_employer_the_main_employer',
            field=models.BooleanField(default=False),
        ),
    ]
