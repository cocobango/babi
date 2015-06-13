# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20150606_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthly_employee_data',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='monthly_employer_data',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
