import datetime

from django.contrib.auth.models import Group
from django.db import models


class Person(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    number = models.CharField(blank=True, max_length=20)
    gender = models.CharField(max_length=7, choices=(('M', 'Male'), ('F', 'Female')))

    class Meta:
        abstract = True


class AttendanceStatus(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            help_text='"Present" will not be saved but will show as a teacher option.')
    code = models.CharField(max_length=10, unique=True,
                            help_text="Short code used on attendance reports. Ex: A might be the code for the "
                                      "name Absent")

    class Meta:
        verbose_name_plural = 'Attendance Statuses'

    def __str__(self):
        return self.name


class Instructor(Person):
    class Meta:
        ordering = ("full_name",)

    def save(self, make_user_group=True, *args, **kwargs):
        self.is_staff = True
        super(Instructor, self).save(*args, **kwargs)
        if make_user_group:
            group, created = Group.objects.get_or_create(name="Faculty")
            self.groups.add(group)

    def __str__(self):
        return "{}".format(self.full_name)


class Student(Person):
    student_id = models.CharField(max_length=10)

    class Meta:
        ordering = ("full_name",)

    def save(self, make_user_group=True, *args, **kwargs):
        self.is_staff = True
        super(Student, self).save(*args, **kwargs)
        if make_user_group:
            group, created = Group.objects.get_or_create(name="Student")
            self.groups.add(group)

    def __str__(self):
        return "{}".format(self.full_name)


class Course(models.Model):
    is_active = models.BooleanField(default=True)
    code = models.CharField(max_length=7, unique=True, verbose_name='Course Code')
    title = models.CharField(max_length=255, unique=True, verbose_name="Course Title")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class CourseSection(models.Model):
    course = models.ForeignKey(Course, related_name='sections')
    is_active = models.BooleanField(default=True)
    section_number = models.PositiveSmallIntegerField()
    teachers = models.ManyToManyField(Instructor, blank=True)
    enrollments = models.ManyToManyField(Student, blank=True)

    def __str__(self):
        return '{} section {}'.format(self.course, self.section_number)


class CourseSectionAttendance(models.Model):
    """
        Attendance taken at each course (section)
    """
    student = models.ForeignKey(Student)
    course_section = models.ForeignKey(CourseSection)
    date = models.DateField(default=datetime.datetime.now)
    time_in = models.TimeField(blank=True, null=True)
    status = models.ForeignKey(AttendanceStatus)
    notes = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.student, self.date, self.status)
