# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0017_auto_20151005_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employer',
            old_name='is_an_npo',
            new_name='is_npo',
        ),
    ]
