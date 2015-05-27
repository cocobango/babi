# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField()),
                ('government_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('business_id', models.IntegerField()),
                ('income_tax_id', models.IntegerField()),
                ('phone_number', models.IntegerField()),
                ('name_of_contact', models.CharField(max_length=200)),
                ('is_required_to_pay_vat', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Monthly_employee_data',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('gross_payment', models.DecimalField(decimal_places=2, max_digits=11)),
                ('travel_expenses', models.DecimalField(decimal_places=2, max_digits=11)),
                ('gross_or_cost', models.BooleanField(default=True)),
                ('is_required_to_pay_social_security', models.BooleanField(default=True)),
                ('is_employer_the_main_employer', models.BooleanField(default=True)),
                ('gross_payment_from_others', models.DecimalField(decimal_places=2, max_digits=11)),
                ('employee', models.ForeignKey(to='reports.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Monthly_employer_data',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_required_to_pay_vat', models.BooleanField(default=True)),
                ('is_required_to_pay_income_tax', models.BooleanField(default=True)),
                ('lower_tax_threshold', models.DecimalField(decimal_places=2, max_digits=11)),
                ('upper_tax_threshold', models.DecimalField(decimal_places=2, max_digits=11)),
                ('income_tax_threshold', models.DecimalField(decimal_places=2, max_digits=11)),
                ('exact_income_tax_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('monthly_employee_data', models.OneToOneField(to='reports.Monthly_employee_data')),
            ],
        ),
        migrations.CreateModel(
            name='Monthly_system_data',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('vat_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('social_security_threshold', models.DecimalField(decimal_places=2, max_digits=11)),
                ('lower_employee_social_security_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('lower_employer_social_security_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('upper_employee_social_security_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('upper_employer_social_security_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('maximal_sum_to_pay_social_security', models.DecimalField(decimal_places=2, max_digits=11)),
                ('income_tax_default', models.DecimalField(decimal_places=2, max_digits=11)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='employer',
            field=models.ForeignKey(to='reports.Employer'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
