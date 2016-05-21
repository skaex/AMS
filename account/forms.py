
from django import forms

class UploadFileForm(forms.Form):
    form = forms.FileField()