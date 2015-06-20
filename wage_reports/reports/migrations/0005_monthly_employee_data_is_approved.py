# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_monthly_employee_data_entered_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthly_employee_data',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
