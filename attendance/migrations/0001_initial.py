# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, help_text='"Present" will not be saved but will show as a teacher option.', max_length=255)),
                ('code', models.CharField(unique=True, help_text='Short code used on attendance reports. Ex: A might be the code for the name Absent', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Attendance Statuses',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.CharField(unique=True, verbose_name='Course Code', max_length=7)),
                ('title', models.CharField(unique=True, verbose_name='Course Title', max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('section_number', models.PositiveSmallIntegerField()),
                ('course', models.ForeignKey(to='attendance.Course', related_name='sections')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSectionAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('time_in', models.TimeField(null=True, blank=True)),
                ('notes', models.CharField(blank=True, max_length=500)),
                ('course_section', models.ForeignKey(to='attendance.CourseSection')),
                ('status', models.ForeignKey(to='attendance.AttendanceStatus')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('number', models.CharField(blank=True, max_length=20)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=7)),
            ],
            options={
                'ordering': ('full_name',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(null=True, blank=True, max_length=254)),
                ('number', models.CharField(blank=True, max_length=20)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=7)),
                ('student_id', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ('full_name',),
            },
        ),
        migrations.AddField(
            model_name='coursesectionattendance',
            name='student',
            field=models.ForeignKey(to='attendance.Student'),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='enrollments',
            field=models.ManyToManyField(to='attendance.Student', blank=True),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='teachers',
            field=models.ManyToManyField(to='attendance.Instructor', blank=True),
        ),
    ]
