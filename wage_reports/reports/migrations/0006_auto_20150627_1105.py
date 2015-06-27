# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_monthly_employee_data_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthly_employee_data',
            name='for_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='monthly_employee_data',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
