# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_auto_20150627_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locked_months',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('for_month', models.IntegerField(default=0)),
                ('for_year', models.IntegerField(default=0)),
                ('lock_time', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(to='reports.Employer')),
            ],
        ),
        migrations.AddField(
            model_name='monthly_employee_data',
            name='for_year',
            field=models.IntegerField(default=0),
        ),
    ]
