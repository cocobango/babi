# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0020_auto_20151024_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthly_employee_data',
            name='is_elderly',
            field=models.BooleanField(default=False),
        ),
    ]
