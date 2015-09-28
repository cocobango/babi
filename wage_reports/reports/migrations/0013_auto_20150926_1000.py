# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0012_auto_20150919_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='is_an_npo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='monthly_employer_data',
            name='entered_by',
            field=models.CharField(max_length=30, default='employer'),
        ),
    ]
