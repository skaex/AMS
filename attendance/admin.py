from django.contrib import admin

from .models import Student, Instructor, Course, CourseSection, CourseSectionAttendance


# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'email', 'gender']
    search_fields = ['student_id', 'full_name', 'email']
    list_filter = ['gender']


class InstructorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'gender']
    search_fields = ['full_name', 'email']
    list_filter = ['gender']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'description']
    search_fields = ['code', 'title', 'description']


class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ['course', 'section_number']
    search_fields = ['course', 'section_number']
    filter_horizontal = ['instructors', 'enrollment']


class CourseSectionAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course_section', 'date', 'status', 'notes']
    search_fields = ['status']
    list_filter = ['student', 'course_section', 'date', 'status']

admin.site.register(Student, StudentAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSection, CourseSectionAdmin)
admin.site.register(CourseSectionAttendance, CourseSectionAttendanceAdmin)
