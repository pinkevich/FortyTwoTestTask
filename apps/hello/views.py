import json

from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404

from .models import Bio, HttpRequest
from .utils import save_requests


@save_requests()
def main(request):
    return render(request, 'main.html', {'bio': Bio.objects.first()})


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
