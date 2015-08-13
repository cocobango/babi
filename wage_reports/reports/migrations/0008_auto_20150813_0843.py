# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_auto_20150627_1633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthly_employer_data',
            name='monthly_employee_data',
        ),
        migrations.AddField(
            model_name='monthly_employer_data',
            name='employee',
            field=models.ForeignKey(to='reports.Employee', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_employer_data',
            name='entered_by',
            field=models.CharField(default='employee', max_length=30),
        ),
        migrations.AddField(
            model_name='monthly_employer_data',
            name='for_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monthly_employer_data',
            name='for_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monthly_employer_data',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='monthly_employer_data',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
