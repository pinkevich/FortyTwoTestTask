import json

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required

from .models import Bio, HttpRequest
from .utils import save_requests
from .forms import BioEditForm


def main(request):
    return render(request, 'main.html')


def http_requests(request):
    if request.is_ajax():
        data = json.dumps({'success': False})
        if request.method == 'GET':
            if not isinstance(data, type(None)):
                data = serialize('json', request.http_requests)
        elif request.method == 'POST':
            req = get_object_or_404(HttpRequest,
                                    pk=request.POST.get('request_pk'))
            if not req.is_read:
                req.is_read = True
                req.save(update_fields=['is_read'])
                data = json.dumps({'success': True})
        return HttpResponse(data)
    return render(request, 'requests.html')


@save_requests()
@login_required()
def edit(request):
    form = BioEditForm(instance=Bio.objects.first())
    if request.is_ajax() and request.method == 'POST':
        form = BioEditForm(request.POST, request.FILES,
                           instance=Bio.objects.first())
        if form.is_valid():
            form.save()
            data = json.dumps({'success': True})
        else:
            data = json.dumps({'success': False, 'errors': form.errors})
        return HttpResponse(data)
    return render(request, 'edit.html', {'form': form})
