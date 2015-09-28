# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_auto_20150926_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monthly_employee_report_data',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('entered_by', models.CharField(max_length=30, default='automatic')),
                ('for_month', models.IntegerField(default=0)),
                ('for_year', models.IntegerField(default=0)),
                ('income_tax', models.DecimalField(max_digits=11, decimal_places=2)),
                ('vat', models.DecimalField(max_digits=11, decimal_places=2)),
                ('input_tax_vat', models.DecimalField(max_digits=11, decimal_places=2)),
                ('employee', models.ForeignKey(to='reports.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Monthly_employee_social_security_report_data',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('sum_to_calculate_as_lower_social_security_percentage', models.DecimalField(max_digits=11, decimal_places=2)),
                ('sum_to_calculate_as_upper_social_security_percentage', models.DecimalField(max_digits=11, decimal_places=2)),
                ('diminished_sum', models.DecimalField(max_digits=11, decimal_places=2)),
                ('standard_sum', models.DecimalField(max_digits=11, decimal_places=2)),
                ('total', models.DecimalField(max_digits=11, decimal_places=2)),
                ('monthly_employee_report_data', models.OneToOneField(to='reports.Monthly_employee_report_data')),
            ],
        ),
    ]
