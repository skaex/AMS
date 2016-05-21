# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('code', models.CharField(unique=True, max_length=7, verbose_name='Course Code')),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='Course Title')),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('section_number', models.PositiveSmallIntegerField()),
                ('course', models.ForeignKey(to='attendance.Course', related_name='sections')),
            ],
        ),
        migrations.CreateModel(
            name='CourseSectionAttendance',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('time_in', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, null=True, choices=[('A', 'Absent'), ('L', 'Late'), ('X', 'Present')], max_length=50)),
                ('notes', models.CharField(blank=True, null=True, max_length=500)),
                ('course_section', models.ForeignKey(to='attendance.CourseSection')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('gender', models.CharField(blank=True, null=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=7)),
                ('email', models.EmailField(blank=True, null=True, max_length=254)),
            ],
            options={
                'ordering': ('full_name',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('gender', models.CharField(blank=True, null=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=7)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('student_id', models.CharField(unique=True, max_length=10)),
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
            name='enrollment',
            field=models.ManyToManyField(blank=True, to='attendance.Student'),
        ),
        migrations.AddField(
            model_name='coursesection',
            name='instructors',
            field=models.ManyToManyField(blank=True, to='attendance.Instructor'),
        ),
    ]
