# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0018_auto_20151010_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locked_months',
            name='first_day_in_month',
        ),
    ]
