from django.core.cache import cache

from .models import HttpRequest


class HttpRequestMiddleware(object):

    def process_request(self, request):
        request.http_requests = cache.get('http_requests')

    def process_response(self, request, response):
        if not request.is_ajax():
            new_requests = HttpRequest.objects.priority_order()
            cache.set('http_requests', new_requests)
        return response
