import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

from attendance.models import CourseSection, Course, Student, Instructor, CourseSectionAttendance
from .attendance import Attendance
from .forms import AttendanceImportForm

@login_required(login_url='admin:login')
def preview_excel(request):
    if request.method == 'POST':
        form = AttendanceImportForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = request.FILES['input_excel']
            path = default_storage.save('tmp/' + str(file_obj), ContentFile(file_obj.read()))
            tmp_file_path = os.path.join(settings.MEDIA_ROOT, path)  # temporarily store excel file on disk

            attendance_sheet = Attendance.get_sheet(tmp_file_path)  # read the file from the remp folder
            attendance_json = Attendance.get_attendance_json(Attendance(), attendance_sheet)
            request.session[
                'get_data'] = attendance_json  # store all the attendance data on a session to be used in another view
            os.remove(tmp_file_path)  # delete the file from the temp folder to free up memory
            return render(request, 'attendance/confirm_file.html', {'attendance_json': attendance_json})
    else:
        form = AttendanceImportForm()
    return render(request, 'attendance/upload.html', {'form': form})

@login_required(login_url='admin:login')
def submit(request):
    # if request.method == 'POST':
    if request.session.get('get_data') is not None:
        attendance_data = request.session.get('get_data')
        course_code = attendance_data['data']['course']['code']
        description = attendance_data['data']['course']['description']
        section = attendance_data['data']['course']['section']
        instructor = attendance_data['data']['course']['instructor']
        instructor, created = Instructor.objects.get_or_create(full_name=instructor)
        course, created = Course.objects.get_or_create(code=course_code, title=description, )
        course_section, created = CourseSection.objects.get_or_create(course=course, section_number=section)
        course_section.instructors.add(instructor)
        for student in attendance_data['data']['attendances']:
            student_id = student['student_aun_id']
            email = student['email']
            full_name = student['names']
            new_student, created = Student.objects.get_or_create(student_id=student_id, email=email,
                                                                 full_name=full_name)
            course_section.enrollment.add(new_student)

            for status in student['statuses']:
                date = status['date']
                att_status = status['status']
                CourseSectionAttendance.objects.get_or_create(student=new_student, course_section=course_section, date=date, status=att_status)
        return render(request, 'attendance/thanks.html', {'thanks': 'Thanks'})
    else:
        form = AttendanceImportForm()
    return render(request, 'attendance/upload.html', {'form': form})

    # else:
    #     form = AttendanceImportForm()
    # return render(request, 'attendance/upload.html', {'form': form})
