# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import datetime 

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_auto_20150815_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthly_system_data',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='monthly_system_data',
            name='for_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='monthly_system_data',
            name='for_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='monthly_employer_data',
            name='exact_income_tax_percentage',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
        migrations.AlterField(
            model_name='monthly_system_data',
            name='income_tax_default',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
        migrations.AlterField(
            model_name='monthly_system_data',
            name='lower_employee_social_security_percentage',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
        migrations.AlterField(
            model_name='monthly_system_data',
            name='lower_employer_social_security_percentage',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
        migrations.AlterField(
            model_name='monthly_system_data',
            name='social_security_threshold',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
        migrations.AlterField(
            model_name='monthly_system_data',
            name='upper_employee_social_security_percentage',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
        migrations.AlterField(
            model_name='monthly_system_data',
            name='upper_employer_social_security_percentage',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
        migrations.AlterField(
            model_name='monthly_system_data',
            name='vat_percentage',
            field=models.DecimalField(decimal_places=8, max_digits=16),
        ),
    ]
