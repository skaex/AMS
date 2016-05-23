import datetime

from django.contrib.auth.models import Group
from django.db import models


class Person(models.Model):
    """
    an abstract base class (model) for holding attributes that are common to other
    models. This model is ignored during migrations, thus doesn't translate into an
    actual database table
    """
    full_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=7, blank=True, null=True, choices=(('M', 'Male'), ('F', 'Female')))

    class Meta:
        abstract = True


# class AttendanceStatus(models.Model):
#     """
#     various attendance status that can be attributed to a student
#     """
#     name = models.CharField(max_length=255, unique=True,
#                             help_text='"Present" will not be saved but will show as a teacher option.')
#     code = models.CharField(max_length=10, unique=True,
#                             help_text="Short code used on attendance reports. Ex: A might be the code for the "
#                                       "name Absent")
#
#     class Meta:
#         verbose_name_plural = 'Attendance Statuses'
#
#     def __str__(self):
#         return self.name
#

class Instructor(Person):
    email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ("full_name",)

    def save(self, make_user_group=True, *args, **kwargs):
        self.is_staff = True
        super(Instructor, self).save(*args, **kwargs)
        if make_user_group:
            group, created = Group.objects.get_or_create(name="Faculty")
            # self.groups.add(group)

    def __str__(self):
        return "{}".format(self.full_name)


class Student(Person):
    email = models.EmailField()
    student_id = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ("full_name",)

    def save(self, make_user_group=True, *args, **kwargs):
        self.is_staff = True
        super(Student, self).save(*args, **kwargs)
        if make_user_group:
            group, created = Group.objects.get_or_create(name="Student")
            # self.groups.add(group)

    def __str__(self):
        return "{}".format(self.full_name)


class Course(models.Model):
    # is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=7, unique=True, verbose_name='Course Code')
    title = models.CharField(max_length=255, unique=True, verbose_name="Course Title")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class CourseSection(models.Model):
    course = models.ForeignKey(Course, related_name='sections')
    # is_active = models.BooleanField(default=True)
    section_number = models.PositiveSmallIntegerField()
    instructors = models.ManyToManyField(Instructor, blank=True)
    enrollment = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return '{} section {}'.format(self.course, self.section_number)


class CourseSectionAttendance(models.Model):
    """
        Attendance taken at each course (section)
    """
    STATUSES = (
        ('A', 'Absent'),
        ('L', 'Late'),
        ('X', 'Present'),
    )
    student = models.ForeignKey(Student)
    course_section = models.ForeignKey(CourseSection)
    date = models.DateTimeField()
    time_in = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True, choices=STATUSES)
    notes = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.student, self.date, self.status)
