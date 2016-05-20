import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

from .attendance import Attendance
from .forms import AttendanceImportForm


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


def submit(request):
    # if request.method == 'POST':
    if request.session.get('get_data') is not None:
        attendance_data = request.session.get('get_data')










        return render(request, 'attendance/thanks.html', {'thanks': thanks})
    else:
        form = AttendanceImportForm()
    return render(request, 'attendance/upload.html', {'form': form})

    # else:
    #     form = AttendanceImportForm()
    # return render(request, 'attendance/upload.html', {'form': form})
