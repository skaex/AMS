# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesectionattendance',
            name='status',
            field=models.ForeignKey(null=True, to='attendance.AttendanceStatus', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='gender',
            field=models.CharField(null=True, max_length=7, choices=[('M', 'Male'), ('F', 'Female')], blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='number',
            field=models.CharField(null=True, max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(null=True, max_length=7, choices=[('M', 'Male'), ('F', 'Female')], blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='number',
            field=models.CharField(null=True, max_length=20, blank=True),
        ),
    ]
