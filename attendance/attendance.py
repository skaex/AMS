import datetime
import re
import sys

import simplejson
import xlrd


class Attendance(object):
    @staticmethod
    def get_date(xl_date):
        """
        converts xl_date to standard datetime
        :param xl_date:
        :return:
        """
        date = datetime.datetime(*xlrd.xldate_as_tuple(xl_date, 0))
        return date

    def get_sheet(self, excel_file):
        """
        gets excel file and extracts the attendance sheet from it
        Asumption: attendance information is always on the first sheet of eact book (excel file)
        :param excel_file:
        :return:
        """
        try:
            book = xlrd.open_workbook(excel_file)
        except:
            print("Failed to open the excel file")
            sys.exit(1)
        attendance_sheet = book.sheet_by_index(0) # assuming attendance is on first sheet
        return attendance_sheet

    def course(self, attendance_sheet):
        """
        This method takes in an attendance sheet as parameter and returns the course information
        including the teacher's name
        :param attendance_sheet:
        :return:
        """
        code = attendance_sheet.cell(1, 1).value
        section = int(attendance_sheet.cell(2, 1).value)
        description = attendance_sheet.cell(3, 1).value
        instructor = attendance_sheet.cell(4, 1).value

        if (re.match(r'^[a-zA-Z]{3}\s*\d{3}$', code) is not None and
                    re.match(r'^[1-9]{1}$', str(section)) is not None and
                    re.match(r"^\s*[a-zA-Z]{1,}([\s-]*[a-zA-Z\s\'-]*)$", description) is not None and
                    re.match(r"^\s*[a-zA-Z]{1,}([\s-]*[a-zA-Z\s\'-\.]*)$", instructor) is not None
            ):

            course_info = {'code': code, 'section': section, 'description': description, 'instructor': instructor}
            return course_info
        else:
            raise Exception('Make sure the course information in cells B2-B5 are correct!')

    def attendances(self, attendance_sheet):
        """
        this method takes in an attendance sheet and extracts the attendance information for each student.
        This attendance information includes the student't information and their attendance status for
        each date during which attendance was taken, ***with a valid date***
        :param attendance_sheet:
        :return:
        """

        attendances = []
        for row in range(0, attendance_sheet.nrows):
            student_id = attendance_sheet.cell(row, 0).value
            names = attendance_sheet.cell(row, 1).value
            email = attendance_sheet.cell(row, 2).value
            if (re.match(r'^(A|a)(0|1)[0]{2}\d{5}$', student_id) is not None and
                        re.match(r"^\s*[a-zA-Z]{1,}([\s-]*[a-zA-Z\s\'-\.]*)$", names) is not None and
                        re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None):

                student = {'student_aun_id': student_id, 'names': names, 'email': email}
                statuses = []
                for col in range(3, attendance_sheet.ncols):
                    # assuming dates alsways begin from cell J6 of each attendance sheet
                    if attendance_sheet.cell(5, col).ctype == xlrd.XL_CELL_DATE:
                        xl_date = attendance_sheet.cell(5, col).value
                        date = str(self.get_date(xl_date))
                        status = attendance_sheet.cell(row, col).value
                        statuses.append({'date': date, 'status': status})

                student['statuses'] = statuses
                attendances.append(student)

        return attendances

    def get_attendance_json(self, attendance_sheet):
        """
        This method takes in an attendance sheet and uses previously defined methods to
        format data into a json
        :param attendance_sheet:
        :return:
        """
        course_data = self.course(attendance_sheet)
        attendance_data = self.attendances(attendance_sheet)
        data = {'data': {'course': course_data, 'attendances': attendance_data}}
        return simplejson.dumps(data)


# uncomment the following lines and use them for testing the script
# att = Attendance()
# file = "path/to/excel/file.xlsx"
# sheet = att.get_sheet(file) #
# attendances = att.attendances(sheet)
# # print(attendances)
# print(att.get_attendance_json(sheet))
