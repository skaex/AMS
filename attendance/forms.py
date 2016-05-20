import os
from django import forms

IMPORT_FILE_TYPES = ['.xls', '.xlsx']


class AttendanceImportForm(forms.Form):
    input_excel = forms.FileField(required=True, label="Upload Excel file.")

    def clean_input_excel(self):
        input_excel = self.cleaned_data['input_excel']
        extension = os.path.splitext(input_excel.name)[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError(
                '{} is not a valid excel file. Please make sure your input file is an excel file'.format(extension))
        else:
            return input_excel


class AttendanceSubmitForm(forms.Form):
    pass
