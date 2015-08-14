# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_auto_20150813_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='locked_months',
            name='first_day_in_month',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 12, 44, 13, 502349, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
