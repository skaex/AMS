from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid:
            form = UploadFileForm(request.POST, request.FILES)
    else:
        form = UploadFileForm()
    return render(request,
                  'account/upload_file.html',
                  {'form': form})
